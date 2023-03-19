from argparse import ArgumentParser
from textwrap import dedent
from other.output import open_csv_file, write_to_csv, print_total
from other.logger import logging, log, set_logging_config
from other.lists import deduplicate_input, invalid_clean_up, invalid_keys
from shodan_api.shodan_api import check as check_shodan, present as present_shodan
from shodan_api.shodan_api import shodan_basic_keys, shodan_dev_keys, shodan_edu_keys, shodan_oss_keys
from censys_api.censys_api import check as check_censys, present as present_censys
from censys_api.censys_api import censys_valid_keys
from virustotal_api.virustotal_api import check as check_virustotal, present as present_virustotal
from virustotal_api.virustotal_api import vt_valid_keys
from binaryedge_api.binaryedge_api import check as check_binaryedge, present as present_binaryedge
from binaryedge_api.binaryedge_api import binaryedge_free_keys, binaryedge_starter_keys, binaryedge_business_keys, binaryedge_enterprise_keys

from rich import print

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input_list", metavar="FILE_NAME", help="Specify shodan API keys list to check, one key per line")
parser.add_argument("-o", "--output", dest="output_list", metavar="FILE_NAME", help="Specify output csv file")
args = parser.parse_args()

if __name__ in "__main__":
    if args.input_list is None:
        print("Please specify file containing list of keys (-i, --input)")
        exit()

    set_logging_config(level=logging.INFO)

    log.info("[bold yellow]Checking keys...[/bold yellow]")
    # Keys deduplication
    keys_to_check = deduplicate_input(args.input_list)
    invalid_keys[0] = keys_to_check
    # Shodan validation
    for key in invalid_keys[0]:
        check_shodan(key, 1)
    invalid_clean_up(0)
    # Censys validation
    for key in invalid_keys[1]:
        check_censys(key, 0)
    invalid_clean_up(1)
    # VirusTotal validation
    for key in invalid_keys[0]:
        check_virustotal(key, 1)
    invalid_clean_up(0)
    # BinaryEdge validation
    for key in invalid_keys[1]:
        check_binaryedge(key, 0)

    output_file = open_csv_file("output" if args.output_list is None else args.output_list)

    # Writing Shodan
    write_to_csv('shodan', shodan_basic_keys, output_file)
    write_to_csv('shodan', shodan_oss_keys, output_file)
    write_to_csv('shodan', shodan_dev_keys, output_file)
    write_to_csv('shodan', shodan_edu_keys, output_file)
    # Writing Censys
    write_to_csv('censys', censys_valid_keys, output_file)
    # Writing VirusTotal
    write_to_csv('virustotal', vt_valid_keys, output_file)
    # Writing BinaryEdge
    write_to_csv('binaryedge', binaryedge_free_keys, output_file)
    write_to_csv('binaryedge', binaryedge_starter_keys, output_file)
    write_to_csv('binaryedge', binaryedge_business_keys, output_file)
    write_to_csv('binaryedge', binaryedge_enterprise_keys, output_file)
    # Present user-friendly output
    present_shodan()
    present_censys()
    present_virustotal()
    present_binaryedge()

        print_total([keys_to_check], app_name='\nTotal Keys:')
        print_total([shodan_basic_keys, shodan_oss_keys, shodan_dev_keys, shodan_edu_keys], app_name='[SHODAN]')
        print_total([censys_valid_keys], app_name='[CENSYS]')
        print_total([vt_valid_keys], app_name='[VIRUSTOTAL]')
        print_total([binaryedge_free_keys, binaryedge_starter_keys, binaryedge_business_keys, binaryedge_enterprise_keys], app_name='[BINARYEDGE]')
        print_total([binaryedge_invalid_keys], is_valid=False)