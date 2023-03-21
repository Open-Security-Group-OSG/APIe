from requests import get
from other.logger import log
from other.output import print_title, print_keys, write_to_csv
from other.lists import invalid_keys
from other.dictionaries import regex
from re import search


class ShodanAPI:
    basic_keys = []
    oss_keys = []
    dev_keys = []
    edu_keys = []

    def __init__(self):
        self.name = 'Shodan'

    def check(self, key: str, list_id: int):
        """Checks if credentials are valid as Shodan API credentials

        :param str key: API key as a string
        :param int list_id: ID of list to be used for invalid keys
        :return: list with key, boolean specifying if key is valid and, if valid, plan name from API call
        """
        try:
            if search(regex[self.name.lower()], key):
                plan = get(f'https://api.shodan.io/api-info?key={key}').json()['plan']
                log.info(f'[bold blue]{key}[/] is a [bold green]VALID[/] [bold yellow]{self.name} KEY[/] and plan is [bold cyan]{str(plan).upper()}[/]')

                match plan.lower():
                    case 'basic':
                        self.basic_keys.append([key, plan])
                    case 'oss':
                        self.oss_keys.append([key, plan])
                    case 'dev':
                        self.dev_keys.append([key, plan])
                    case 'edu':
                        self.edu_keys.append([key, plan])
                    case _:
                        invalid_keys[list_id].append(key)
                        log.warning(f'[bold yellow][ATTENTION][/] Weird key detected - [bold red]{key}[/], plan is [bold cyan]{plan}[/], [bold red]manual verification required[/]')
                return [key, True, plan]
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
        if self.basic_keys:
            print_title('Shodan', 'BASIC')
            print_keys(self.basic_keys, keep_status=False)
        if self.oss_keys:
            print_title('Shodan', 'OSS')
            print_keys(self.oss_keys, keep_status=False)
        if self.dev_keys:
            print_title('Shodan', 'DEV')
            print_keys(self.dev_keys, keep_status=False)
        if self.edu_keys:
            print_title('Shodan', 'EDU')
            print_keys(self.edu_keys, keep_status=False)

    def write(self, output_file: str):
        """Writes valid credentials

        :param str output_file: csv file to write valid credentials to
        :return: appends valid credentials to specified csv file
        """
        write_to_csv('shodan', self.basic_keys, output_file)
        write_to_csv('shodan', self.oss_keys, output_file)
        write_to_csv('shodan', self.dev_keys, output_file)
        write_to_csv('shodan', self.edu_keys, output_file)
