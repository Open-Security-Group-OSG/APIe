from requests import get
from other.logger import log
from other.output import print_title, print_keys, write_to_csv
from other.lists import invalid_keys

shodan_basic_keys = []
shodan_oss_keys = []
shodan_dev_keys = []
shodan_edu_keys = []


def check(key: str, list_id: int):
    try:
        key_plan = get(f'https://api.shodan.io/api-info?key={key}').json()['plan']
        log.info(f'[bold blue]{key}[/] is a [bold green]VALID[/] [bold yellow]SHODAN KEY[/] and plan is [bold cyan]{str(key_plan).upper()}[/]')

        match key_plan.lower():
            case 'basic':
                shodan_basic_keys.append([key, key_plan])
            case 'oss':
                shodan_oss_keys.append([key, key_plan])
            case 'dev':
                shodan_dev_keys.append([key, key_plan])
            case 'edu':
                shodan_edu_keys.append([key, key_plan])
            case _:
                invalid_keys[list_id].append(key)
                log.warning(f'[bold yellow][ATTENTION][/] Weird key detected - [bold red]{key}[/], plan is [bold cyan]{key_plan}[/], [bold red]manual verification required[/]')
        return [key, True, key_plan]
    except:
        log.info(f'[bold blue]{key}[/] is [bold red]INVALID[/] as [bold yellow]SHODAN KEY[/]')
        invalid_keys[list_id].append(key)
        return [key, False]


def present():
    if shodan_basic_keys:
        print_title('Shodan', 'BASIC')
        print_keys(shodan_basic_keys, keep_status=False)
    if shodan_oss_keys:
        print_title('Shodan', 'OSS')
        print_keys(shodan_oss_keys, keep_status=False)
    if shodan_dev_keys:
        print_title('Shodan', 'DEV')
        print_keys(shodan_dev_keys, keep_status=False)
    if shodan_edu_keys:
        print_title('Shodan', 'EDU')
        print_keys(shodan_edu_keys, keep_status=False)


def write(output_file: str):
    write_to_csv('shodan', shodan_basic_keys, output_file)
    write_to_csv('shodan', shodan_oss_keys, output_file)
    write_to_csv('shodan', shodan_dev_keys, output_file)
    write_to_csv('shodan', shodan_edu_keys, output_file)