import requests
import json
import os
import subprocess
import sys

from colorama import Fore, init

__version__ = 1.7

languages = {
    'da'    : 'Danish',
    'de'    : 'German',
    'en-GB' : 'English, UK',
    'en-US' : 'English, US',
    'es-ES' : 'Spanish',
    'fr'    : 'French',
    'hr'    : 'Croatian',
    'lt'    : 'Lithuanian',
    'hu'    : 'Hungarian',
    'nl'    : 'Dutch',
    'no'    : 'Norwegian',
    'pl'    : 'Polish',
    'pt-BR' : 'Portuguese, Brazilian',
    'ro'    : 'Romanian, Romania',
    'fi'    : 'Finnish',
    'sv-SE' : 'Swedish',
    'vi'    : 'Vietnamese',
    'tr'    : 'Turkish',
    'cs'    : 'Czech',
    'el'    : 'Greek',
    'bg'    : 'Bulgarian',
    'ru'    : 'Russian',
    'uk'    : 'Ukranian',
    'th'    : 'Thai',
    'zh-CN' : 'Chinese, China',
    'ja'    : 'Japanese',
    'zh-TW' : 'Chinese, Taiwan',
    'ko'    : 'Korean'
}

def main():
    init(convert=True) # makes console support ANSI escape color codes

    #print('\33]0;Discord Token Info by WodX\a', end='', flush=True) # changes console title

    #subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True) # clears console

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
                }
            )
                
            if res.status_code == 200: # code 200 if valid
                res_json = json.loads(res.text)

                user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                user_id = res_json['id']
                avatar_id = res_json['avatar']
                phone_number = res_json['phone']
                email = res_json['email']
                mfa_enabled = res_json['mfa_enabled']
                flags = res_json['flags']
                locale = res_json['locale']
                verified = res_json['verified']
                language = languages.get(locale)

                print('Basic Information')
                print('-----------------')
                print(f'    {Fore.RESET}User Name              {Fore.GREEN}{user_name}')
                print(f'    {Fore.RESET}User ID                {Fore.GREEN}{user_id}')
                print(f'    {Fore.RESET}Avatar ID              {Fore.GREEN}{avatar_id if avatar_id else ""}')
                print(f'    {Fore.RESET}Avatar URL             {Fore.GREEN}{f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.webp" if avatar_id else ""}')
                print(f'    {Fore.RESET}Mention                {Fore.GREEN}<@{user_id}>')
                print(f'{Fore.RESET}\n')

                print('Contact Information')
                print('-------------------')
                print(f'    {Fore.RESET}Phone Number           {Fore.YELLOW}{phone_number if phone_number else ""}')
                print(f'    {Fore.RESET}Email                  {Fore.YELLOW}{email if email else ""}')
                print(f'{Fore.RESET}\n')

                print('Account Security')
                print('----------------')
                print(f'    {Fore.RESET}2FA/MFA Enabled        {Fore.BLUE}{mfa_enabled}')
                print(f'    {Fore.RESET}Flags                  {Fore.BLUE}{flags}')
                print(f'{Fore.RESET}\n')

                print('Other')
                print('-----')
                print(f'    {Fore.RESET}Locale                 {Fore.RED}{locale} ({language})')
                print(f'    {Fore.RESET}Verified               {Fore.RED}{verified}')

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
