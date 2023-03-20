from other.output import print_total
from other.lists import invalid_keys
from APIs.binaryedge_api import BinaryEdgeAPI
from APIs.censys_api import present as present_censys
from APIs.censys_api import censys_valid_keys
from APIs.fofa_api import FofaAPI
from APIs.shodan_api import present as present_shodan
from APIs.shodan_api import shodan_basic_keys, shodan_oss_keys, shodan_dev_keys, shodan_edu_keys
from APIs.virustotal_api import present as present_virustotal
from APIs.virustotal_api import vt_valid_keys


def present_valid_keys():
    # List every API here
    BinaryEdgeAPI().present()
    present_censys()
    FofaAPI().present()
    present_shodan()
    present_virustotal()


def print_totals():
    # List every API here
    print_total([BinaryEdgeAPI().free_keys, BinaryEdgeAPI().starter_keys, BinaryEdgeAPI().business_keys, BinaryEdgeAPI().enterprise_keys], app_name='\n[BINARYEDGE]')
    print_total([censys_valid_keys], app_name='[CENSYS] ')
    print_total([FofaAPI().valid_keys], app_name=f'[{FofaAPI().name}] ')
    print_total([shodan_basic_keys, shodan_oss_keys, shodan_dev_keys, shodan_edu_keys], app_name='[SHODAN] ')
    print_total([vt_valid_keys], app_name='[VIRUSTOTAL] ')
    # Total Invalid Keys
    print_total([invalid_keys[0]], is_valid=False, app_name='[bold blue]')
