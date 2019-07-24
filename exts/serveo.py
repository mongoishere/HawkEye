from time import sleep
from subprocess import Popen, call, check_output, PIPE
import sys, os, re

class Serveo(object):

    def __init__(self):
        pass

    def test_serveo(self):
        check_output('ssh -o \
            StrictHostKeyChecking=no -o \
            ServerAliveInterval=60 -o \
            ServerAliveCountMax=60 -R \
            80:localhost:1337 serveo.net 1> link.url 2> /dev/null &', shell=True)

        sleep(10)
        
        try:
            serveo_url = check_output("cat link.url", shell=True)
            serveo_url = re.search('http\S+', str(serveo_url))[0]
            serveo_url = serveo_url[0:serveo_url.find("\\r\\")]

            import pdb; pdb.set_trace()

        except Exception as e:
            print(str(e))
    
        #running_serveos = []; running_serveos = str(running_serveos).split('\\n')
        
        target_pids  = []

        running_serveos = check_output("ps aux | grep -i 'Strict'", shell=True)
        running_serveos = str(running_serveos).split('\\n')

        #for process in running_serveos:
            #import pdb; pdb.set_trace(header='Process Break')
        
        for process in running_serveos:
                try: target_pids.append(process.split(' '*6)[1].split()[0])
                except IndexError:
                    print(process.split())
                    target_pids.append(process.split()[1])
                    import pdb; pdb.set_trace(header='Exception Break')
                

if __name__ == '__main__':

    app = Serveo()
    app.test_serveo()