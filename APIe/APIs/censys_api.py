from requests import get
from requests.auth import HTTPBasicAuth
from other.logger import log
from other.output import print_title, print_keys, write_to_csv
from other.lists import invalid_keys
from other.dictionaries import regex
from re import search


class CensysAPI:
    valid_keys = []

    def __init__(self):
        self.name = 'Censys'

    def check(self, id_and_secret: str, list_id: int):
        """Checks if credentials are valid as Censys API credentials

        :param str id_and_secret: id and secret key pair os one string separated by ':'
        :param int list_id: ID of list to be used for invalid keys
        :return: list with id_and_secret, boolean specifying if key pair is valid and, if valid, allowance from API call
        """
        credentials = id_and_secret.split(':')

        try:
            id_and_secret_reversed = f'{credentials[1]}:{credentials[0]}'
        except:
            log.info(f'[bold blue]{id_and_secret}[/] are [bold red]INVALID[/] as [bold yellow]CENSYS CREDENTIALS[/] due to lacks second value')
            invalid_keys[list_id].append(id_and_secret)
            return [id_and_secret, False]
        try:
            if search(regex[self.name.lower()], id_and_secret):
                allowance = get(f'https://search.censys.io/api/v1/account', auth=HTTPBasicAuth(credentials[0], credentials[1])).json()['quota']['allowance']
                log.info(f'[bold cyan]ID:[/] [bold blue]{credentials[0]}[/] [bold cyan]SECRET:[/] [bold blue]{credentials[1]}[/] are [bold green]VALID[/] as [bold yellow]{self.name} CREDENTIALS[/] and have allowance of [bold cyan]{allowance}[/]')
                self.valid_keys.append([id_and_secret, allowance])
                return [id_and_secret, True, allowance]

            elif search(regex[self.name.lower()], id_and_secret_reversed):
                allowance = get(f'https://search.censys.io/api/v1/account', auth=HTTPBasicAuth(credentials[1], credentials[0])).json()['quota']['allowance']
                log.info(f'[bold cyan]ID:[/] [bold blue]{credentials[1]}[/] [bold cyan]SECRET:[/] [bold blue]{credentials[0]}[/] are [bold green]VALID[/]  as [bold yellow]{self.name} CREDENTIALS[/] and have allowance of [bold cyan]{allowance}[/]')
                self.valid_keys.append([id_and_secret_reversed, allowance])
                return [id_and_secret_reversed, True, allowance]

            else:
                log.info(f'[bold blue]{id_and_secret}[/] are [bold red]INVALID[/] as [bold yellow]{self.name} CREDENTIALS[/] according to regex')
                invalid_keys[list_id].append(id_and_secret)
                return [id_and_secret, False]
        except:
            log.info(
                f'[bold blue]{id_and_secret}[/] are [bold red]INVALID[/] as [bold yellow]{self.name} CREDENTIALS[/] according to API call')
            invalid_keys[list_id].append(id_and_secret)
            return [id_and_secret, False]

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