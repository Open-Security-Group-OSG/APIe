from requests import get
from other.logger import log
from other.output import print_title, print_keys, write_to_csv
from other.lists import invalid_keys
from other.dictionaries import regex
from re import search


class BinaryEdgeAPI:  # TODO Remove API name from lists below
    free_keys = []
    starter_keys = []
    business_keys = []
    enterprise_keys = []

    def __init__(self):
        self.name = 'BinaryEdge'

    def check(self, key: str, list_id: int):
        """Checks if credentials are valid as BinaryEdge API credentials

        :param str key: API key as a string
        :param int list_id: ID of list to be used for invalid keys
        :return: list with key, boolean specifying if key is valid and, if valid, subscription name from API call
        """
        try:
            if search(regex[self.name.lower()], key):
                subscription = get('https://api.binaryedge.io/v2/user/subscription', headers={'X-Key': f'{key}'}).json()['subscription']['name']
                log.info(f'[bold blue]{key}[/] is a [bold green]VALID[/] [bold yellow]{self.name} KEY[/] and plan is [bold cyan]{str(subscription).upper()}[/]')

                match subscription.lower():
                    case 'free':
                        self.free_keys.append([key, subscription])
                    case 'starter':
                        self.starter_keys.append([key, subscription])
                    case 'business':
                        self.business_keys.append([key, subscription])
                    case 'enterprise':
                        self.enterprise_keys.append([key, subscription])
                    case _:
                        invalid_keys[list_id].append(key)
                        log.warning(f'[bold yellow][ATTENTION][/] Weird key detected - [bold red]{key}[/], plan is [bold cyan]{subscription}[/], [bold red]manual verification required[/]')
                return [key, True, subscription]
            else:
                log.info(f'[bold blue]{key}[/] is [bold red]INVALID[/] as [bold yellow]{self.name} KEY[/] according to regex')
                invalid_keys[list_id].append(key)
                return [key, False]
        except:
            log.info(f'[bold blue]{key}[/] is [bold red]INVALID[/] as [bold yellow]{self.name} KEY[/] according to API call')
            invalid_keys[list_id].append(key)
            return [key, False]

    def present(self):
        """Visually presents all valid credentials in terminal

        :return: visual representation of valid credentials
        """
        if self.free_keys:
            print_title('BinaryEdge', 'FREE')
            print_keys(self.free_keys, keep_status=False)
        if self.starter_keys:
            print_title('BinaryEdge', 'STARTER')
            print_keys(self.starter_keys, keep_status=False)
        if self.business_keys:
            print_title('BinaryEdge', 'BUSINESS')
            print_keys(self.business_keys, keep_status=False)
        if self.enterprise_keys:
            print_title('BinaryEdge', 'ENTERPRISE')
            print_keys(self.enterprise_keys, keep_status=False)

    def write(self, output_file: str):
        """Writes valid credentials

        :param str output_file: csv file to write valid credentials to
        :return: appends valid credentials to specified csv file
        """
        write_to_csv('binaryedge', self.free_keys, output_file)
        write_to_csv('binaryedge', self.starter_keys, output_file)
        write_to_csv('binaryedge', self.business_keys, output_file)
        write_to_csv('binaryedge', self.enterprise_keys, output_file)
