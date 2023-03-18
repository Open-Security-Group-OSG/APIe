from argparse import ArgumentParser
import csv
from other.style import bold_cyan, bold_green, bold_red, reset
from shodan_api.shodan import check as check_shodan
from shodan_api.shodan_api import shodan_basic_keys, shodan_dev_keys, shodan_edu_keys, shodan_oss_keys, shodan_invalid_keys
from censys_api.censys_api import check as check_censys
from censys_api.censys_api import censys_valid_keys, censys_invalid_keys

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input_list", metavar="FILE_NAME" , help="Specify shodan API keys list to check, one key per line")
parser.add_argument("-o", "--output", dest="output_list", metavar="FILE_NAME", help="Specify output csv file")
args = parser.parse_args()

if __name__ in "__main__":
    if args.input_list is None:
        print("Please specify file containing list of keys")
        exit()
    print("Checking keys..")
    with open(args.input_list, 'r') as keys_list:
        deduplicated = list(dict.fromkeys(keys_list.readlines()))
        keys_to_check = []
        
        for key in deduplicated:
            new_key = key.replace("\n", "")
            keys_to_check.append(new_key)

        for key in keys_to_check:
            key = key.strip()
            result = check_shodan(key)
        
            if result[1] is False:
                shodan_invalid_keys.append(result[0])
            elif result[2] == 'dev':
                shodan_dev_keys.append(result[0])
            elif result[2] == 'edu':
                shodan_edu_keys.append(result[0])
            elif result[2] == 'oss':
                shodan_oss_keys.append(result[0])
            elif result[2] == 'basic':
                shodan_basic_keys.append(result[0])
            else:
                shodan_invalid_keys.append(result[0])

        # Censys validation begins
        for key in shodan_invalid_keys:
            result = check_censys(key)
            
            if result[1] is False:
                censys_invalid_keys.append(result[0])
            elif result[1] is True:
                censys_valid_keys.append([result[0], result[2]])
            else:
                censys_invalid_keys.append(result[0])

        output_name = "output.csv" if args.output_list == None else args.output_list
        output_name = f'{output_name}.csv' if 'csv' not in output_name else output_name
        with open(output_name, 'w') as output_list:
            keys_writer = csv.writer(output_list)
            keys_writer.writerow(['app', 'key', 'info'])
            for key in shodan_dev_keys:
                keys_writer.writerow(['shodan', key, 'DEV'])
            for key in shodan_edu_keys:
                keys_writer.writerow(['shodan', key, 'EDU'])
            for key in shodan_oss_keys:
                keys_writer.writerow(['shodan', key, 'OSS'])
            for key in shodan_basic_keys:
                keys_writer.writerow(['shodan', key, 'BASIC'])
            for key in censys_valid_keys:
                keys_writer.writerow(['censys', key[0], key[1]])

        print(f'\n{bold_cyan}[+] Valid SHODAN DEV Keys{reset}')
        for i in shodan_dev_keys: print(i)
        print(f'\n{bold_cyan}[+] Valid SHODAN EDU Keys{reset}')
        for i in shodan_edu_keys: print(i)
        print(f'\n{bold_cyan}[+] Valid SHODAN OSS Keys{reset}')
        for i in shodan_oss_keys: print(i)
        print(f'\n{bold_cyan}[+] Valid SHODAN BASIC Keys{reset}')
        for i in shodan_basic_keys: print(i)
        print(f'\n{bold_cyan}[+] Valid CENSYS Keys{reset}')
        for i in censys_valid_keys: print(f'{i[0]} {i[1]}')

        print(f"\nTotal keys: {bold_cyan}{len(keys_to_check)}{reset}")
        print(f"{bold_cyan}[SHODAN]{reset} DEV keys: {bold_green}{len(shodan_dev_keys)}{reset}, EDU keys: {bold_green}{len(shodan_edu_keys)}{reset}, OSS keys: {bold_green}{len(shodan_oss_keys)}{reset}, BASIC keys: {bold_green}{len(shodan_basic_keys)}{reset}")
        print(f"{bold_cyan}[CENSYS]{reset} Valid keys: {bold_green}{len(censys_valid_keys)}{reset}")
        print(f"Invalid keys: {bold_red}{len(censys_invalid_keys)}")
