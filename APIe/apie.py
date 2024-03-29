from argparse import ArgumentParser
from other.output import open_csv_file
from other.logger import logging, log, set_logging_config
from other.lists import deduplicate_input, invalid_clean_up, invalid_keys
from other.user.output import present_valid_keys, print_totals
from APIs.binaryedge_api import BinaryEdgeAPI
from APIs.censys_api import CensysAPI
from APIs.fofa_api import FofaAPI
from APIs.shodan_api import ShodanAPI
from APIs.virustotal_api import VirusTotalAPI


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

    # List every API here
    for key in invalid_keys[0]:
        BinaryEdgeAPI().check(key, 1)
    invalid_clean_up(0)

    for key in invalid_keys[1]:
        CensysAPI().check(key, 0)
    invalid_clean_up(1)

    for key in invalid_keys[0]:
        FofaAPI().check(key, 1)
    invalid_clean_up(0)

    for key in invalid_keys[1]:
        ShodanAPI().check(key, 0)
    invalid_clean_up(1)

    for key in invalid_keys[0]:
        VirusTotalAPI().check(key, 1)

    output_file = open_csv_file("output" if args.output_list is None else args.output_list)

    # List every API here
    BinaryEdgeAPI().write(output_file)
    CensysAPI().write(output_file)
    FofaAPI().write(output_file)
    ShodanAPI().write(output_file)
    VirusTotalAPI().write(output_file)

    # Present user-friendly output
    present_valid_keys()
    print_totals()
