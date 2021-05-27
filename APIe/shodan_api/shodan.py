import shodan
from other.style import bold_green, bold_red, bold_cyan, reset

def check(key: str):
    api = shodan.Shodan(key)
    try:
        key_plan = api.info()['plan']
        print(f'{key} is {bold_green}VALID{reset} and {bold_cyan}{str(key_plan).upper()}{reset}')
        return [key, True, key_plan]
    except:
        print(f'{key} is {bold_red}INVALID{reset}')
        return [key, False]

