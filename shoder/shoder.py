import shodan
from argparse import ArgumentParser

COLORS = {
    "RED":"\u001b[31m",
    "GREEN":"\u001b[32m",
    "CYAN":"\u001b[36m",
    "RESET":"\u001b[0m",
    "BOLD":"\u001b[1m"
}
bold_green = f"{COLORS['BOLD']}{COLORS['GREEN']}"
bold_red = f"{COLORS['BOLD']}{COLORS['RED']}"
bold_cyan = f"{COLORS['BOLD']}{COLORS['CYAN']}"
reset = COLORS['RESET']

parser = ArgumentParser()
parser.add_argument("-l", "--list", dest="input_list", metavar="FILE_NAME" , help="Specify shodan API keys list to check, one key per line")
args = parser.parse_args()


def check(key: str):
    api = shodan.Shodan(key)
    try:
        key_plan = api.info()['plan']
        print(f'{key} is {bold_green}VALID{reset} and {bold_cyan}{str(key_plan).upper()}{reset}')
        return [key, True, key_plan]
    except:
        print(f'{key} is {bold_red}INVALID{reset}')
        return [key, False]

if __name__ in "__main__":
    if args.input_list is None:
        print("Please specify file containing list of keys")
        exit()
    print("Checking keys..")
    with open(f'{args.input_list}', 'r') as keys_list:
        deduplicated = list(dict.fromkeys(keys_list.readlines()))
        keys_to_check = []
        dev_keys = []
        edu_keys = []
        oss_keys = []
        invalid_keys = []
        for key in deduplicated:
            new_key = key.replace("\n", "")
            keys_to_check.append(new_key)

        for key in keys_to_check:
            key = key.strip()
            result = check(key)
        
            if result[1] is False:
                invalid_keys.append(result[0])
            elif result[2] == 'dev':
                dev_keys.append(result[0])
            elif result[2] == 'edu':
                edu_keys.append(result[0])
            elif result[2] == 'oss':
                oss_keys.append(result[0])
            else:
                pass



        print(f'\n{bold_cyan}[+] Valid DEV Keys{reset}')
        for i in dev_keys: print(i)
        print(f'\n{bold_cyan}[+] Valid EDU Keys{reset}')
        for i in edu_keys: print(i)
        print(f'\n{bold_cyan}[+] Valid OSS Keys{reset}')
        for i in edu_keys: print(i)
        print(f"\nTotal keys: {bold_cyan}{len(keys_to_check)}{reset}")
        print(f"DEV keys: {bold_green}{len(dev_keys)}{reset}, EDU keys: {bold_green}{len(edu_keys)}{reset}, OSS keys: {bold_green}{len(oss_keys)}{reset}")
        print(f"Invalid keys: {bold_red}{len(invalid_keys)}")
