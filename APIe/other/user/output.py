from other.output import print_total
from other.lists import invalid_keys
from APIs.binaryedge_api import BinaryEdgeAPI
from APIs.censys_api import CensysAPI
from APIs.fofa_api import FofaAPI
from APIs.shodan_api import ShodanAPI
from APIs.virustotal_api import present as present_virustotal
from APIs.virustotal_api import vt_valid_keys


def present_valid_keys():
    # List every API here
    BinaryEdgeAPI().present()
    CensysAPI().present()
    FofaAPI().present()
    ShodanAPI().present()
    present_virustotal()


def print_totals():
    # List every API here
    print_total([BinaryEdgeAPI().free_keys, BinaryEdgeAPI().starter_keys, BinaryEdgeAPI().business_keys, BinaryEdgeAPI().enterprise_keys], app_name=f'\n[{BinaryEdgeAPI().name}] ')
    print_total([CensysAPI().valid_keys], app_name=f'[{CensysAPI().name}] ')
    print_total([FofaAPI().valid_keys], app_name=f'[{FofaAPI().name}] ')
    print_total([ShodanAPI().basic_keys, ShodanAPI().oss_keys, ShodanAPI().dev_keys, ShodanAPI().edu_keys], app_name=f'[{ShodanAPI().name}] ')
    print_total([vt_valid_keys], app_name='[VIRUSTOTAL] ')
    # Total Invalid Keys
    print_total([invalid_keys[0]], is_valid=False, app_name='[bold blue]')
