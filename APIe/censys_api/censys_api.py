from requests import get
from requests.auth import HTTPBasicAuth
from other.style import bold_green, bold_red, bold_cyan, bold_yellow, reset
censys_valid_keys = []
censys_invalid_keys = []


def check(id_and_secret: str):
    credentials = id_and_secret.split(':')
    try:
        allowance = get(f'https://search.censys.io/api/v1/account', auth=HTTPBasicAuth(credentials[0], credentials[1])).json()['quota']['allowance']
        print(f'{bold_cyan}ID:{reset} {credentials[0]} {bold_cyan}SECRET:{reset} {credentials[1]} is a {bold_green}VALID{reset} {bold_yellow}CENSYS KEY{reset} and has allowance of {bold_cyan}{allowance}{reset}')
        censys_valid_keys.append([id_and_secret, allowance])

        return [id_and_secret, True, allowance]
    except:
        print(f'{id_and_secret} is {bold_red}INVALID{reset} as {bold_yellow}CENSYS KEY{reset}')
        censys_invalid_keys.append(id_and_secret)
        return [id_and_secret, False]
