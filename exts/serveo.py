from time import sleep
from subprocess import Popen, call, check_output, PIPE
import sys, os, re

class Serveo(object):

    def __init__(self):
        pass

    @classmethod
    def kill_serveo(self, pid):
        return(call(f'kill -9 {int(pid)}', shell=True))

    def run_serveo(self, port):
        check_output(f'ssh -o \
            StrictHostKeyChecking=no -o \
            ServerAliveInterval=60 -o \
            ServerAliveCountMax=60 -R \
            80:localhost:{port} serveo.net 1> link.url 2> /dev/null &', shell=True)

        sleep(10)
        
        try:
            serveo_url = check_output("cat link.url", shell=True)
            serveo_url = re.search('http\S+', str(serveo_url))[0]
            serveo_url = serveo_url[0:serveo_url.find("\\r\\")]

        except Exception as e:
            print(str(e))

        yield serveo_url
        
        target_pids  = []

        running_serveos = check_output("ps aux | grep -i 'StrictHostKeyChecking=no'", shell=True)
        running_serveos = str(running_serveos).split('\\n')
        
        for process in running_serveos[:-1]:
            try: target_pids.append(process.split(' '*6)[1].split()[0])
            except IndexError:
                print(process)
                if (process.split()[0] == '"'): break
                else: target_pids.append(process.split(' '*5)[1].split()[0]); continue
                target_pids.append(process.split()[1])

        for pid in target_pids[:-1]:
            import pdb; pdb.set_trace(header=f'Killing Process: {pid}')
            self.kill_serveo(pid)
   
        

if __name__ == '__main__':

    app = Serveo()
    app.test_serveo()