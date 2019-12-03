import requests
import json
import os
import subprocess
import sys

from colorama import Fore, init

__version__ = 1.5

languages = {
    'DA'    : 'Danish',
    'DE'    : 'German',
    'EN-GB' : 'English, UK',
    'EN-US' : 'English, US',
    'ES-ES' : 'Spanish',
    'FR'    : 'French',
    'HR'    : 'Croatian',
    'LT'    : 'Lithuanian',
    'HU'    : 'Hungarian',
    'NL'    : 'Dutch',
    'NO'    : 'Norwegian',
    'PL'    : 'Polish',
    'PT-BR' : 'Portuguese, Brazilian',
    'RO'    : 'Romanian, Romania',
    'FI'    : 'Finnish',
    'SV-SE' : 'Swedish',
    'VI'    : 'Vietnamese',
    'TR'    : 'Turkish',
    'CS'    : 'Czech',
    'EL'    : 'Greek',
    'BG'    : 'Bulgarian',
    'RU'    : 'Russian',
    'UK'    : 'Ukranian',
    'TH'    : 'Thai',
    'ZH-CN' : 'Chinese, China',
    'JA'    : 'Japanese',
    'ZH-TW' : 'Chinese, Taiwan',
    'KO'    : 'Korean'
}

def main():
    init(convert=True) # makes console support ANSI escape color codes

    print('\33]0;Discord Token Info by WodX\a', end='', flush=True) # changes console title

    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True) # clears console

    print('''
    {0}██████{1}╗ {0}████████{1}╗{0}██{1}╗
    {0}██{1}╔══{0}██{1}╗╚══{0}██{1}╔══╝{0}██{1}║
    {0}██{1}║  {0}██{1}║   {0}██{1}║   {0}██{1}║
    {0}██{1}║  {0}██{1}║   {0}██{1}║   {0}██{1}║
    {0}██████{1}╔╝   {0}██{1}║   {0}██{1}║
    {1}╚═════╝    ╚═╝   ╚═╝ {4}v{3}

   {1}Discord Token Info Tool
          {4}by WodX{2}
    '''.format(Fore.CYAN, Fore.WHITE, Fore.RESET, __version__, Fore.YELLOW))

    if len(sys.argv) == 2:
        token = sys.argv[1]
        try:

            # sends request
            res = requests.get(
                url='https://discordapp.com/api/v6/users/@me',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/53',
                    'Authorization': token,
                    'Content-Type': 'application/json'
                })
                
            if res.status_code == 200: # code 200 if valid
                res_json = json.loads(res.text)

                print('Basic Information')
                print('-----------------')
                print(f'    {Fore.RESET}Username               {Fore.GREEN}{res_json["username"]}#{res_json["discriminator"]}')
                print(f'    {Fore.RESET}User ID                {Fore.GREEN}{res_json["id"]}')
                avatar = res_json['avatar']
                print(f'    {Fore.RESET}Avatar                 {Fore.GREEN}{avatar if avatar else ""}')
                
                print(f'{Fore.RESET}\n')
                print('Contact Information')
                print('-------------------')
                phone = res_json['phone']
                print(f'    {Fore.RESET}Phone Number           {Fore.YELLOW}{phone if phone else ""}')
                email = res_json['email']
                print(f'    {Fore.RESET}Email                  {Fore.YELLOW}{email if email else ""}')
                
                print(f'{Fore.RESET}\n')
                print('Account Security')
                print('----------------')
                print(f'    {Fore.RESET}2FA/MFA Enabled        {Fore.BLUE}{res_json["mfa_enabled"]}')
                print(f'    {Fore.RESET}Flags                  {Fore.BLUE}{res_json["flags"]}')

                print(f'{Fore.RESET}\n')
                print('Other')
                print('-----')
                locale = res_json['locale'].upper()
                print(f'    {Fore.RESET}Locale                 {Fore.RED}{locale} ({languages.get(locale)})')
                print(f'    {Fore.RESET}Verified               {Fore.RED}{res_json["verified"]}')

            elif res.status_code == 401: # code 401 if invalid
                print(f'{Fore.RED}[-] {Fore.RESET}Invalid token')

            else:
                print(f'{Fore.RED}[-] {Fore.RESET}An error occurred while sending request')
        except:
            print(f'{Fore.RED}[-] {Fore.RESET}An error occurred while sending request')
    else:
        print(f'Usage: python {sys.argv[0]} <token>')

if __name__ == '__main__':
    main()
