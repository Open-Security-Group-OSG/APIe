from requests import get
from other.logger import log

vt_valid_keys = []
vt_invalid_keys = []


def check(key: str):
    try:
        allowance = get(f'https://virustotal.com/api/v3/users/{key}', headers={'x-apikey': key}).json()['data']['attributes']['quotas']['api_requests_daily']['allowed']
        log.info(f'[bold blue]{key}[/bold blue] is a [bold green]VALID[/bold green] [bold yellow]VIRUSTOTAL KEY[/bold yellow] and daily requests quota is [bold cyan]{allowance}[/bold cyan]')
        vt_valid_keys.append([key, allowance])

        return [key, True, allowance]
    except:
        log.info(f'[bold blue]{key}[/bold blue] is [bold red]INVALID[/bold red] as [bold yellow]VIRUSTOTAL KEY[/bold yellow]')

        vt_invalid_keys.append(key)
        return [key, False]
