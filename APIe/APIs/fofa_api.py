from requests import get
from other.logger import log
from other.output import print_title, print_keys, write_to_csv
from other.lists import invalid_keys
from other.dictionaries import regex
from re import search


class FofaAPI:
    valid_keys = []

    def __init__(self):
        self.name = 'FOFA'

    def check(self, email_and_key: str, list_id: int):
        """Checks if credentials are valid as FOFA API credentials

        :param str email_and_key: email and key pair as one string separated by ':'
        :param int list_id: ID of list to be used for invalid keys
        :return: list with email_and_key, boolean specifying if key pair is valid and, if valid, vip_level from API call
        """
        credentials = email_and_key.split(':')

        try:
            email_and_key_reversed = f'{credentials[1]}:{credentials[0]}'
        except:
            log.info(f'[bold blue]{email_and_key}[/] are [bold red]INVALID[/] as [bold yellow]{self.name} CREDENTIALS[/] due to lacks second value')
            invalid_keys[list_id].append(email_and_key)
            return [email_and_key, False]

        try:
            if search(regex[self.name.lower()], email_and_key):
                vip_level = get(f'https://fofa.info/api/v1/info/my?email={credentials[0]}&key={credentials[1]}').json()['vip_level']
                log.info(f'[bold cyan]EMAIL:[/] [bold blue]{credentials[0]}[/] [bold cyan]KEY:[/] [bold blue]{credentials[1]}[/] are [bold green]VALID[/] [bold yellow]{self.name} CREDENTIALS[/] and their vip level is [bold cyan]{vip_level}[/]')
                self.valid_keys.append([email_and_key, vip_level])
                return [email_and_key, True, vip_level]

            elif search(regex[self.name.lower()], email_and_key_reversed):
                vip_level = get(f'https://fofa.info/api/v1/info/my?email={credentials[1]}&key={credentials[0]}').json()['vip_level']
                log.info(f'[bold cyan]EMAIL:[/] [bold blue]{credentials[1]}[/] [bold cyan]KEY:[/] [bold blue]{credentials[0]}[/] are [bold green]VALID[/] [bold yellow]{self.name} CREDENTIALS[/] and their vip level is [bold cyan]{vip_level}[/]')
                self.valid_keys.append([email_and_key_reversed, vip_level])
                return [email_and_key_reversed, True, vip_level]

            else:
                log.info(f'[bold blue]{email_and_key}[/] are [bold red]INVALID[/] as [bold yellow]{self.name} CREDENTIALS[/] according to regex')
                invalid_keys[list_id].append(email_and_key)
                return [email_and_key, False]
        except:
            log.info(f'[bold blue]{email_and_key}[/] are [bold red]INVALID[/] as [bold yellow]{self.name} CREDENTIALS[/] according to API call')
            invalid_keys[list_id].append(email_and_key)
            return [email_and_key, False]

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
