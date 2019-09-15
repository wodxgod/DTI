import requests, json, os, subprocess, sys
from colorama import Fore, init

#Version of Discord Token Info Tool
__version__ = 1.0

def main():
    #Makes console support ANSI escape color codes
    init(convert=True)

    #Changing console title
    print('\33]0;Discord Token Info by WodX\a', end='', flush=True)

    #Clearing console
    subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

    #Printing ASCII art banner
    print('''
    {0}██████{1}╗ {0}████████{1}╗{0}██{1}╗
    {0}██{1}╔══{0}██{1}╗╚══{0}██{1}╔══╝{0}██{1}║
    {0}██{1}║  {0}██{1}║   {0}██{1}║   {0}██{1}║
    {0}██{1}║  {0}██{1}║   {0}██{1}║   {0}██{1}║
    {0}██████{1}╔╝   {0}██{1}║   {0}██{1}║
    {1}╚═════╝    ╚═╝   ╚═╝ {4}v{3}

   {1}Discord Token Info Tool
          {4}By WodX{2}
    '''.format(Fore.CYAN, Fore.WHITE, Fore.RESET, __version__, Fore.YELLOW))

    if len(sys.argv) == 2:
        token = sys.argv[1]
        try:

            #Sending request
            res = requests.get(
                url='https://discordapp.com/api/v6/users/@me',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/53',
                    'Authorization': token,
                    'Content-Type': 'application/json'
                })
                
            if res.status_code == 200: #200 if valid

                #Converting response into a JSON object
                res_json = json.loads(res.text)

                #Printing response
                print('Basic Information')
                print('-----------------')
                print(f'    {Fore.RESET}Username               {Fore.GREEN}{res_json["username"]}')
                print(f'    {Fore.RESET}Discriminator          {Fore.GREEN}{res_json["discriminator"]}')
                print(f'    {Fore.RESET}ID                     {Fore.GREEN}{res_json["id"]}')
                print(f'    {Fore.RESET}Avatar                 {Fore.GREEN}{res_json["avatar"]}')
                
                print(f'{Fore.RESET}')
                print('Contact Information')
                print('-------------------')
                print(f'    {Fore.RESET}Phone Number           {Fore.GREEN}{res_json["phone"]}')
                print(f'    {Fore.RESET}Email                  {Fore.GREEN}{res_json["email"]}')
                
                print(f'{Fore.RESET}\n')
                print('Account Security')
                print('----------------')
                print(f'    {Fore.RESET}2FA/MFA Enabled        {Fore.GREEN}{res_json["mfa_enalbed"]}')
                print(f'    {Fore.RESET}Flags                  {Fore.GREEN}{res_json["flags"]}')

                print(f'{Fore.RESET}\n')
                print('Other')
                print('-----')
                print(f'    {Fore.RESET}Locale                 {Fore.GREEN}{res_json["locale"]}')
                print(f'    {Fore.RESET}Verified               {Fore.GREEN}{res_json["verified"]}')

            elif res.status_code == 401: #401 if invalid
                print(f'{Fore.RED}[-] {Fore.RESET}Invalid token')

            else:
                print(f'{Fore.RED}[-] {Fore.RESET}An error occurred while sending request')
        except:
            print(f'{Fore.RED}[-] {Fore.RESET}An error occurred while sending request')
    else:
        print(f'Usage: python {sys.argv[0]} <token>')

if __name__ == '__main__':
    main()