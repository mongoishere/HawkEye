from time import sleep
from zipfile import ZipFile
from shlex import split
from urllib.error import URLError
from urllib.request import urlopen
from contextlib import contextmanager
from subprocess import Popen, call, PIPE
from sys import platform
from platform import architecture

MAGENTA, BLUE, RED, WHITE, CYAN, GREEN, DEFAULT  = '\033[35m', '\u001b[34;1m' , '\033[1;91m', '\033[46m', '\033[36m', '\033[1;32m',  '\033[0m'


class Ngrok(object):
    
    def __init__(self):
        self.select_arrow = f'{BLUE}⮞{DEFAULT} '

    @property
    def installed(self):
        return(not(call('test -f ./bin/ngrok', stderr=PIPE, shell=True)))

    @classmethod
    def kill_ngrok(self, pid):
        return(call(f'kill -9 {int(pid)}', shell=True))

    @classmethod
    def find_ngrok_file(self, os, arch):
        ngrok_base_url = 'https://bin.equinox.io/c/4VmDzA7iaHb/'

        if (os.lower() == 'android') or ('arm' in Popen('uname -a', stdout=PIPE, shell=True).communicate()[0].decode('utf-8')): 
            print('ARM architecture detected\n'); ngrok_file = f'ngrok-stable-linux-arm.zip'

        elif arch == '64bit': ngrok_file = f'ngrok-stable-{os}-amd64.zip'

        else: ngrok_file = f'ngrok-stable-{os}-386.zip'

        ngrok_file = ngrok_base_url + ngrok_file

        return(ngrok_file)

    @classmethod
    def test_ngrok(self):

        call('ngrok http 1337 > /dev/null &', shell=True)
        sleep(2)
        ngrok_proc = Popen(f"ps aux | grep -i 'ngrok http'", stdout=PIPE, shell=True)
        ngrok_pout = ngrok_proc.communicate()
        ngrok_pid = int((ngrok_pout[0].decode('utf-8')).split()[1])
        ngrok_cmd = ngrok_pout[0].decode('utf-8').split()[10:13]
        ngrok_cmd = ' '.join(map(str, ngrok_cmd))

        ngrok_ran = bool(ngrok_cmd == 'ngrok http 1337')

        if ngrok_ran: self.kill_ngrok(int(ngrok_pid))

        return bool(ngrok_cmd == 'ngrok http 1337')
        
    def install_ngrok(self):
        
        install_url = self.find_ngrok_file(platform, architecture()[0])
        ngrok_blob = urlopen(install_url).read()
        with open('ngrok.zip', 'wb') as putfile:
            putfile.write(ngrok_blob)
        zipf = ZipFile('ngrok.zip')
        zipf.extractall('.')
        zipf.close()
        
        call("chmod +x ngrok && rm -rf ngrok.zip", shell=True)

        if not bool(call("mkdir bin; mv ngrok ./bin", shell=True, stderr=PIPE)): print('Successfully installed ngrok')
        else: print('Installation failed...try running with sudo?'); exit(1)

        ngrok_token = str(input(f'Enter Ngrok Authorization Token {self.select_arrow}'))

        if not bool(call(['ngrok', 'authtoken', ngrok_token], shell=False)):
            print('Testing Authtoken...')
            if not(self.test_ngrok()):
                print(f"{RED} Ngrok failed to start...check authorization token{DEFAULT}")
                print('Reinstalling ngrok...')
                call('rm -rf ./bin/ngrok', shell=True)
                self.install_ngrok()
            else: print("Authorized successfully")


    @contextmanager
    def run(self, port):

        if not isinstance(port, int):
            raise TypeError("Port must be an integer")

        start_cmd = f"./bin/ngrok http {port} > /dev/null &"
        ret_val = call(start_cmd, shell=True)
        ngrok_url = None
        while not(ngrok_url):
            ngrok_url = Popen('curl -s -N http://127.0.0.1:4040/api/tunnels | grep "https://[0-9a-z]*\.ngrok.io" -oh ', stdout=PIPE, shell=True)
            ngrok_url = (ngrok_url.stdout.read()).decode('utf-8')[:-1]
        ngrok_proc = Popen(f"ps aux | grep -i 'ngrok http'", stdout=PIPE, shell=True)
        ngrok_pout = ngrok_proc.communicate()
        ngrok_pid = int((ngrok_pout[0].decode('utf-8')).split()[1])
        
        yield ngrok_url

        self.kill_ngrok(int(ngrok_pid))