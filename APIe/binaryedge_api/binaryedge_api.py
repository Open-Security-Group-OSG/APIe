from requests import get
from other.style import bold_green, bold_red, bold_cyan, bold_yellow, reset

binaryedge_free_keys = []
binaryedge_starter_keys = []
binaryedge_business_keys = []
binaryedge_enterprise_keys = []
binaryedge_invalid_keys = []


def check(key: str):
    try:
        key_plan = get('https://api.binaryedge.io/v2/user/subscription', headers={'X-Key':f'{key}'}).json()['subscription']['name']
        print(f'{key} is a {bold_green}VALID{reset} {bold_yellow}BINARYEDGE KEY{reset} and plan is {bold_cyan}{str(key_plan).upper()}{reset}')
        match key_plan.lower():
            case 'free':
                binaryedge_free_keys.append(key)
            case 'starter':
                binaryedge_starter_keys.append(key)
            case 'business':
                binaryedge_starter_keys.append(key)
            case 'enterprise':
                binaryedge_enterprise_keys.append(key)
            case _:
                binaryedge_invalid_keys.append(key)
                print(f'{bold_yellow}[ATTENTION]{reset} Weird key detected - {bold_red}{key}{reset}, plan is {bold_cyan}{key_plan}{reset}, {bold_red}manual verification required{reset}')

        return [key, True, key_plan]
    except:
        print(f'{key} is {bold_red}INVALID{reset} as {bold_yellow}BINARYEDGE KEY{reset}')
        binaryedge_invalid_keys.append(key)
        return [key, False]
