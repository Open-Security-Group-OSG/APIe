from argparse import ArgumentParser
import csv
from textwrap import dedent
from other.style import bold_cyan, bold_green, bold_red, bold_yellow, reset
from shodan_api.shodan_api import check as check_shodan
from shodan_api.shodan_api import shodan_basic_keys, shodan_dev_keys, shodan_edu_keys, shodan_oss_keys, shodan_invalid_keys
from censys_api.censys_api import check as check_censys
from censys_api.censys_api import censys_valid_keys, censys_invalid_keys
from virustotal_api.virustotal_api import check as check_virustotal
from virustotal_api.virustotal_api import vt_valid_keys, vt_invalid_keys
from binaryedge_api.binaryedge_api import check as check_binaryedge
from binaryedge_api.binaryedge_api import binaryedge_free_keys, binaryedge_starter_keys, binaryedge_business_keys, binaryedge_enterprise_keys, binaryedge_invalid_keys

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input_list", metavar="FILE_NAME" , help="Specify shodan API keys list to check, one key per line")
parser.add_argument("-o", "--output", dest="output_list", metavar="FILE_NAME", help="Specify output csv file")
args = parser.parse_args()

if __name__ in "__main__":
    if args.input_list is None:
        print("Please specify file containing list of keys (-i, --input)")
        exit()
    print("Checking keys..")
    # Keys deduplication
    with open(args.input_list, 'r') as keys_list:
        deduplicated = list(dict.fromkeys(keys_list.readlines()))
        keys_to_check = []

        # Shodan validation
        for key in deduplicated:
            keys_to_check.append(key.replace("\n", ""))

        for key in keys_to_check:
            check_shodan(key.strip())

        # Censys validation
        for key in shodan_invalid_keys:
            check_censys(key)

        # VirusTotal validation
        # VirusTotal validation begins
        for key in censys_invalid_keys:
            result = check_virustotal(key)

            if result[1] is False:
                vt_invalid_keys.append(result[0])
            elif result[1] is True:
                vt_valid_keys.append([result[0], result[2]])
            else:
                vt_invalid_keys.append(result[0])
                print(f'{bold_yellow}[ATTENTION]{reset} Weird key detected - {bold_red}{result[0]}{reset}, {bold_red}manual verification required{reset}')
        # BinaryEdge validation begins
        for key in vt_invalid_keys:
            check_binaryedge(key)


        output_name = "output.csv" if args.output_list is None else args.output_list
        output_name = f'{output_name}.csv' if 'csv' not in output_name else output_name
        with open(output_name, 'w') as output_list:  # TODO Move out of main file
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
            for key in vt_valid_keys:
                keys_writer.writerow(['virustotal', key[0], key[1]])
            for key in binaryedge_free_keys:
                keys_writer.writerow(['binaryedge', key, 'Free'])
            for key in binaryedge_starter_keys:
                keys_writer.writerow(['binaryedge', key, 'Starter'])
            for key in binaryedge_business_keys:
                keys_writer.writerow(['binaryedge', key, 'Business'])
            for key in binaryedge_enterprise_keys:
                keys_writer.writerow(['binaryedge', key, 'Enterprise'])

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
        print(f'\n{bold_cyan}[+] Valid VirusTotal Keys{reset}')
        for i in vt_valid_keys: print(f'{i[0]} {i[1]}')
        print(f'\n{bold_cyan}[+] Valid BINARYEDGE FREE Keys{reset}')
        for i in binaryedge_free_keys: print(i)
        print(f'\n{bold_cyan}[+] Valid BINARYEDGE STARTER Keys{reset}')
        for i in binaryedge_starter_keys: print(i)
        print(f'\n{bold_cyan}[+] Valid BINARYEDGE BUSINESS Keys{reset}')
        for i in binaryedge_business_keys: print(i)
        print(f'\n{bold_cyan}[+] Valid BINARYEDGE ENTERPRISE Keys{reset}')
        for i in binaryedge_enterprise_keys: print(i)

        print(f"\nTotal keys: {bold_cyan}{len(keys_to_check)}{reset}")
        print(" ".join(dedent(f"""{bold_cyan}[SHODAN]{reset} 
            DEV keys: {bold_green}{len(shodan_dev_keys)}{reset}, 
            EDU keys: {bold_green}{len(shodan_edu_keys)}{reset}, 
            OSS keys: {bold_green}{len(shodan_oss_keys)}{reset}, 
            BASIC keys: {bold_green}{len(shodan_basic_keys)}{reset}""").replace('\n', '').split()))
        print(f"{bold_cyan}[CENSYS]{reset} Valid keys: {bold_green}{len(censys_valid_keys)}{reset}")
        print(f"{bold_cyan}[VIRUSTOTAL]{reset} Valid keys: {bold_green}{len(vt_valid_keys)}{reset}")
        print(" ".join(dedent(f"""{bold_cyan}[BINARYEDGE]{reset} 
            FREE keys: {bold_green}{len(binaryedge_free_keys)}{reset}, 
            STARTER keys: {bold_green}{len(binaryedge_starter_keys)}{reset}, 
            BUSINESS keys: {bold_green}{len(binaryedge_business_keys)}{reset}, 
            ENTERPRISE keys: {bold_green}{len(binaryedge_enterprise_keys)}{reset}""").replace('\n', '').split()))
        print(f"Invalid keys: {bold_red}{len(censys_invalid_keys)}{reset}")
