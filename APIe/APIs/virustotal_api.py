from requests import get
from other.logger import log
from other.output import print_title, print_keys, write_to_csv
from other.lists import invalid_keys
from other.dictionaries import regex
from re import search


class VirusTotalAPI:
    valid_keys = []

    def __init__(self):
        self.name = 'VirusTotal'

    def check(self, key: str, list_id: int):
        """Checks if credentials are valid as VirusTotal API credentials

        :param str key: API key as a string
        :param int list_id: ID of list to be used for invalid keys
        :return: list with key, boolean specifying if key is valid and, if valid, allowance from API call
        """
        try:
            if search(regex[self.name.lower()], key):
                allowance = get(f'https://virustotal.com/api/v3/users/{key}', headers={'x-apikey': key}).json()['data']['attributes']['quotas']['api_requests_daily']['allowed']
                log.info(f'[bold blue]{key}[/] is a [bold green]VALID[/] [bold yellow]{self.name} KEY[/] and daily requests quota is [bold cyan]{allowance}[/]')
                self.valid_keys.append([key, allowance])
                return [key, True, allowance]

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
        if self.valid_keys:
            print_title(self.name)
            print_keys(self.valid_keys)

    def write(self, output_file: str):
        """Writes valid credentials

        :param str output_file: csv file to write valid credentials to
        :return: appends valid credentials to specified csv file
        """
        write_to_csv(self.name.lower(), self.valid_keys, output_file)
