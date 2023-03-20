from requests import get
from requests.auth import HTTPBasicAuth
from other.logger import log
from other.output import print_title, print_keys, write_to_csv
from other.lists import invalid_keys
from other.dictionaries import regex
from re import search

censys_valid_keys = []


def check(id_and_secret: str, list_id: int):
    credentials = id_and_secret.split(':')

    try:
        id_and_secret_reversed = f'{credentials[1]}:{credentials[0]}'
    except:
        log.info(f'[bold blue]{id_and_secret}[/] is [bold red]INVALID[/] as [bold yellow]CENSYS KEY[/] due to lacks second value')
        invalid_keys[list_id].append(id_and_secret)
        return [id_and_secret, False]
    try:
        if search(regex['censys'], id_and_secret):
            allowance = get(f'https://search.censys.io/api/v1/account', auth=HTTPBasicAuth(credentials[0], credentials[1])).json()['quota']['allowance']
            log.info(f'[bold cyan]ID:[/] [bold blue]{credentials[0]}[/] [bold cyan]SECRET:[/] [bold blue]{credentials[1]}[/] is a [bold green]VALID[/] [bold yellow]CENSYS KEY[/] and has allowance of [bold cyan]{allowance}[/]')
            censys_valid_keys.append([id_and_secret, allowance])
            return [id_and_secret, True, allowance]

        elif search(regex['censys'], id_and_secret_reversed):
            allowance = get(f'https://search.censys.io/api/v1/account', auth=HTTPBasicAuth(credentials[1], credentials[0])).json()['quota']['allowance']
            log.info(f'[bold cyan]ID:[/] [bold blue]{credentials[1]}[/] [bold cyan]SECRET:[/] [bold blue]{credentials[0]}[/] is a [bold green]VALID[/] [bold yellow]CENSYS KEY[/] and has allowance of [bold cyan]{allowance}[/]')
            censys_valid_keys.append([id_and_secret_reversed, allowance])
            return [id_and_secret_reversed, True, allowance]

        else:
            log.info(f'[bold blue]{id_and_secret}[/] is [bold red]INVALID[/] as [bold yellow]CENSYS KEY[/] according to regex')
            invalid_keys[list_id].append(id_and_secret)
            return [id_and_secret, False]
    except:
        log.info(f'[bold blue]{id_and_secret}[/] is [bold red]INVALID[/] as [bold yellow]CENSYS KEY[/] according to API call')
        invalid_keys[list_id].append(id_and_secret)
        return [id_and_secret, False]


def present():
    if censys_valid_keys:
        print_title('Censys')
        print_keys(censys_valid_keys)


def write(output_file: str):
    write_to_csv('censys', censys_valid_keys, output_file)