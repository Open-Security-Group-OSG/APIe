from requests import get
from other.logger import log
from other.output import print_title, print_keys, write_to_csv
from other.lists import invalid_keys
from other.dictionaries import regex
from re import search

vt_valid_keys = []


def check(key: str, list_id: int):
    try:
        if search(regex['virustotal'], key):
            allowance = get(f'https://virustotal.com/api/v3/users/{key}', headers={'x-apikey': key}).json()['data']['attributes']['quotas']['api_requests_daily']['allowed']
            log.info(f'[bold blue]{key}[/] is a [bold green]VALID[/] [bold yellow]VIRUSTOTAL KEY[/] and daily requests quota is [bold cyan]{allowance}[/]')
            vt_valid_keys.append([key, allowance])

            return [key, True, allowance]
        else:
            log.info(f'[bold blue]{key}[/] is [bold red]INVALID[/] as [bold yellow]VIRUSTOTAL KEY[/] according to regex')
            invalid_keys[list_id].append(key)
            return [key, False]
    except:
        log.info(f'[bold blue]{key}[/] is [bold red]INVALID[/] as [bold yellow]VIRUSTOTAL KEY[/] according to API call')
        invalid_keys[list_id].append(key)
        return [key, False]


def present():
    if vt_valid_keys:
        print_title('VirusTotal')
        print_keys(vt_valid_keys)


def write(output_file: str):
    write_to_csv('virustotal', vt_valid_keys, output_file)