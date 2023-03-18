from requests import get
from other.style import bold_green, bold_red, bold_cyan, bold_yellow, reset

shodan_dev_keys = []
shodan_edu_keys = []
shodan_oss_keys = []
shodan_basic_keys = []
shodan_invalid_keys = []


def check(key: str):
    try:
        key_plan = get(f'https://api.shodan.io/api-info?key={key}').json()['plan']
        print(f'{key} is a {bold_green}VALID{reset} {bold_yellow}SHODAN KEY{reset} and plan is {bold_cyan}{str(key_plan).upper()}{reset}')
        return [key, True, key_plan]
    except:
        print(f'{key} is {bold_red}INVALID{reset} as {bold_yellow}SHODAN KEY{reset}')
        return [key, False]
