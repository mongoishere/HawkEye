from time import sleep
from zipfile import ZipFile
from shlex import split
from urllib.error import URLError
from urllib.request import urlopen
from contextlib import contextmanager
from subprocess import Popen, call, PIPE
from sys import platform

MAGENTA, BLUE, RED, WHITE, CYAN, GREEN, DEFAULT  = '\033[35m', '\u001b[34;1m' , '\033[1;91m', '\033[46m', '\033[36m', '\033[1;32m',  '\033[0m'

platforms = {
    'linux': 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip',
    'osx': 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip'
}

class Ngrok(object):

    @property
    def installed(self):
        return(not(call(["which", "ngrok"], stderr=PIPE)))

    @classmethod
    def kill_ngrok(self, pid):
        return(call(f'kill -9 {int(pid)}', shell=True))

    @classmethod
    def test_ngrok(self):

        call('ngrok http 1337 > /dev/null &', shell=True)
        sleep(.5)
        ngrok_proc = Popen(f"ps aux | grep -i 'ngrok http'", stdout=PIPE, shell=True)
        ngrok_pout = ngrok_proc.communicate()
        ngrok_pid = int((ngrok_pout[0].decode('utf-8')).split()[1])

        ngrok_cmd = ngrok_pout[0].decode('utf-8').split()[10:13]
        ngrok_cmd = ' '.join(map(str, ngrok_cmd))

        ngrok_ran = bool(ngrok_cmd == 'ngrok http 1337')

        if ngrok_ran: self.kill_ngrok(int(ngrok_pid))

        return bool(ngrok_cmd == 'ngrok http 1337')
        
    def install_ngrok(self):
        download_url = platforms[platform]
        ngrok_blob = urlopen(download_url).read()
        with open('ngrok.zip', 'wb') as putfile:
            putfile.write(ngrok_blob)
        zipf = ZipFile('ngrok.zip')
        zipf.extractall('.')
        zipf.close()
        
        call("chmod +x ngrok && rm -rf ngrok.zip", shell=True)
        
        if not bool(call('mv ngrok /usr/bin/', stderr=PIPE, shell=True)): print('Successfully installed ngrok')
        else: print('Installation failed...try running with sudo?'); exit(1)

        ngrok_token = str(input('Enter Ngrok Authorization Token >> '))

        if not bool(call(['ngrok', 'authtoken', ngrok_token], shell=False)):
            print('Testing Authtoken...')
            if not(self.test_ngrok()):
                print(f"{RED} Ngrok failed to start...check authorization token{DEFAULT}")
                print('Reinstalling ngrok...')
                call('rm -rf /usr/bin/ngrok', shell=True)
                self.install_ngrok()
            else: print("Authorized successfully")


    @contextmanager
    def run_ngrok(self, port):

        if not isinstance(port, int):
            raise TypeError("Port must be an integer")

        start_cmd = f"ngrok http {port} > /dev/null &"
        call(start_cmd, shell=True)
        sleep(.5)
        ngrok_proc = Popen(f"ps aux | grep -i 'ngrok http'", stdout=PIPE, shell=True)
        ngrok_pout = ngrok_proc.communicate()
        ngrok_pid = int((ngrok_pout[0].decode('utf-8')).split()[1])
        
        yield

        self.kill_ngrok(int(ngrok_pid))

        #call("")