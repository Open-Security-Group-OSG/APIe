from requests import get
from requests.auth import HTTPBasicAuth
from other.logger import log
censys_valid_keys = []
censys_invalid_keys = []


def check(id_and_secret: str):
    credentials = id_and_secret.split(':')
    try:
        allowance = get(f'https://search.censys.io/api/v1/account', auth=HTTPBasicAuth(credentials[0], credentials[1])).json()['quota']['allowance']
        log.info(f'[bold cyan]ID:[/bold cyan] [bold blue]{credentials[0]}[/bold blue] [bold cyan]SECRET:[/bold cyan] [bold blue]{credentials[1]}[/bold blue] is a [bold green]VALID[/bold green] [bold yellow]CENSYS KEY[/bold yellow] and has allowance of [bold cyan]{allowance}[/bold cyan]')

        censys_valid_keys.append([id_and_secret, allowance])

        return [id_and_secret, True, allowance]
    except:
        log.info(f'[bold blue]{id_and_secret}[/bold blue] is [bold red]INVALID[/bold red] as [bold yellow]CENSYS KEY[/bold yellow]')

        censys_invalid_keys.append(id_and_secret)
        return [id_and_secret, False]
