import requests
import json
import sys

from datetime import datetime
from colorama import Fore, init

__version__ = 1.9

languages = {
    'da'    : 'Danish, Denmark',
    'de'    : 'German, Germany',
    'en-GB' : 'English, United Kingdom',
    'en-US' : 'English, United States',
    'es-ES' : 'Spanish, Spain',
    'fr'    : 'French, France',
    'hr'    : 'Croatian, Croatia',
    'lt'    : 'Lithuanian, Lithuania',
    'hu'    : 'Hungarian, Hungary',
    'nl'    : 'Dutch, Netherlands',
    'no'    : 'Norwegian, Norway',
    'pl'    : 'Polish, Poland',
    'pt-BR' : 'Portuguese, Brazilian, Brazil',
    'ro'    : 'Romanian, Romania',
    'fi'    : 'Finnish, Finland',
    'sv-SE' : 'Swedish, Sweden',
    'vi'    : 'Vietnamese, Vietnam',
    'tr'    : 'Turkish, Turkey',
    'cs'    : 'Czech, Czechia, Czech Republic',
    'el'    : 'Greek, Greece',
    'bg'    : 'Bulgarian, Bulgaria',
    'ru'    : 'Russian, Russia',
    'uk'    : 'Ukranian, Ukraine',
    'th'    : 'Thai, Thailand',
    'zh-CN' : 'Chinese, China',
    'ja'    : 'Japanese',
    'zh-TW' : 'Chinese, Taiwan',
    'ko'    : 'Korean, Korea'
}

cc_digits = {
    'american express': '3',
    'visa': '4',
    'mastercard': '5'
}

def main():
    init(convert=True) # makes console support ANSI escape color codes

    print('''
    {0}██████{1}╗ {0}████████{1}╗{0}██{1}╗
    {0}██{1}╔══{0}██{1}╗╚══{0}██{1}╔══╝{0}██{1}║
    {0}██{1}║  {0}██{1}║   {0}██{1}║   {0}██{1}║
    {0}██{1}║  {0}██{1}║   {0}██{1}║   {0}██{1}║
    {0}██████{1}╔╝   {0}██{1}║   {0}██{1}║
    {1}╚═════╝    ╚═╝   ╚═╝ {4}v{3}

   {1}Discord Token Info Tool
          {4}by wodx{2}
    '''.format(Fore.CYAN, Fore.WHITE, Fore.RESET, __version__, Fore.YELLOW))

    if len(sys.argv) == 2:
        token = sys.argv[1]

        try:
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json'
            }

            res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)

            if res.status_code == 200: # code 200 if valid

                # user info
                res_json = res.json()

                user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
                user_id = res_json['id']
                avatar_id = res_json['avatar']
                avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.gif'
                phone_number = res_json['phone']
                email = res_json['email']
                mfa_enabled = res_json['mfa_enabled']
                flags = res_json['flags']
                locale = res_json['locale']
                verified = res_json['verified']
                
                language = languages.get(locale)

                creation_date = datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')

                has_nitro = False
                res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
                nitro_data = res.json()
                has_nitro = bool(len(nitro_data) > 0)
                if has_nitro:
                    d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                    d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                    days_left = abs((d2 - d1).days)

                # billing info
                billing_info = []
                for x in requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers).json():
                    y = x['billing_address']
                    name = y['name']
                    address_1 = y['line_1']
                    address_2 = y['line_2']
                    city = y['city']
                    postal_code = y['postal_code']
                    state = y['state']
                    country = y['country']

                    if x['type'] == 1:
                        cc_brand = x['brand']
                        cc_first = cc_digits.get(cc_brand)
                        cc_last = x['last_4']
                        cc_month = str(x['expires_month'])
                        cc_year = str(x['expires_year'])
                        
                        data = {
                            'Payment Type': 'Credit Card',
                            'Valid': not x['invalid'],
                            'CC Holder Name': name,
                            'CC Brand': cc_brand.title(),
                            'CC Number': ''.join(z if (i + 1) % 2 else z + ' ' for i, z in enumerate((cc_first if cc_first else '*') + ('*' * 11) + cc_last)),
                            'CC Exp. Date': ('0' + cc_month if len(cc_month) < 2 else cc_month) + '/' + cc_year[2:4],
                            'Address 1': address_1,
                            'Address 2': address_2 if address_2 else '',
                            'City': city,
                            'Postal Code': postal_code,
                            'State': state if state else '',
                            'Country': country,
                            'Default Payment Method': x['default']
                        }

                    elif x['type'] == 2:
                        data = {
                            'Payment Type': 'PayPal',
                            'Valid': not x['invalid'],
                            'PayPal Name': name,
                            'PayPal Email': x['email'],
                            'Address 1': address_1,
                            'Address 2': address_2 if address_2 else '',
                            'City': city,
                            'Postal Code': postal_code,
                            'State': state if state else '',
                            'Country': country,
                            'Default Payment Method': x['default']
                        }

                    billing_info.append(data)

                print('Basic Information')
                print('-----------------')
                print(f'    {Fore.RESET}Username               {Fore.GREEN}{user_name}')
                print(f'    {Fore.RESET}User ID                {Fore.GREEN}{user_id}')
                print(f'    {Fore.RESET}Creation Date          {Fore.GREEN}{creation_date}')
                print(f'    {Fore.RESET}Avatar URL             {Fore.GREEN}{avatar_url if avatar_id else ""}')
                print(f'    {Fore.RESET}Token                  {Fore.GREEN}{token}')
                print(f'{Fore.RESET}\n')
                
                print('Nitro Information')
                print('-----------------')
                print(f'    {Fore.RESET}Nitro Status           {Fore.MAGENTA}{has_nitro}')
                if has_nitro:
                    print(f'    {Fore.RESET}Expires in             {Fore.MAGENTA}{days_left} day(s)')
                print(f'{Fore.RESET}\n')


                print('Contact Information')
                print('-------------------')
                print(f'    {Fore.RESET}Phone Number           {Fore.YELLOW}{phone_number if phone_number else ""}')
                print(f'    {Fore.RESET}Email                  {Fore.YELLOW}{email if email else ""}')
                print(f'{Fore.RESET}\n')

                if len(billing_info) > 0:
                    print('Billing Information')
                    print('-------------------')
                    if len(billing_info) == 1:
                        for x in billing_info:
                            for key, val in x.items():
                                if not val:
                                    continue
                                print(Fore.RESET + '    {:<23}{}{}'.format(key, Fore.CYAN, val))
                    else:
                        for i, x in enumerate(billing_info):
                            title = f'Payment Method #{i + 1} ({x["Payment Type"]})'
                            print('    ' + title)
                            print('    ' + ('=' * len(title)))
                            for j, (key, val) in enumerate(x.items()):
                                if not val or j == 0:
                                    continue
                                print(Fore.RESET + '        {:<23}{}{}'.format(key, Fore.CYAN, val))
                            if i < len(billing_info) - 1:
                                print(f'{Fore.RESET}\n')
                    print(f'{Fore.RESET}\n')

                print('Account Security')
                print('----------------')
                print(f'    {Fore.RESET}2FA/MFA Enabled        {Fore.BLUE}{mfa_enabled}')
                print(f'    {Fore.RESET}Flags                  {Fore.BLUE}{flags}')
                print(f'{Fore.RESET}\n')

                print('Other')
                print('-----')
                print(f'    {Fore.RESET}Locale                 {Fore.RED}{locale} ({language})')
                print(f'    {Fore.RESET}Email Verified         {Fore.RED}{verified}')

            elif res.status_code == 401: # code 401 if invalid
                print(f'{Fore.RED}[-] {Fore.RESET}Invalid token')

            else:
                print(f'{Fore.RED}[-] {Fore.RESET}An error occurred while sending request')
        except:
            print(f'{Fore.RED}[-] {Fore.RESET}An error occurred while getting request')
    else:
        print(f'Usage: python {sys.argv[0]} [token]')

if __name__ == '__main__':
    main()