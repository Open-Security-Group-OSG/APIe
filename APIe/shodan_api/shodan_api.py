from requests import get
from other.logger import log

shodan_basic_keys = []
shodan_oss_keys = []
shodan_dev_keys = []
shodan_edu_keys = []
shodan_invalid_keys = []


def check(key: str):
    try:
        key_plan = get(f'https://api.shodan.io/api-info?key={key}').json()['plan']
        log.info(f'[bold blue]{key}[/bold blue] is a [bold green]VALID[/bold green] [bold yellow]SHODAN KEY[/bold yellow] and plan is [bold cyan]{str(key_plan).upper()}[/bold cyan]')

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
                shodan_invalid_keys.append(key)
                log.warning(f'[bold yellow][ATTENTION][/bold yellow] Weird key detected - [bold red]{key}[/bold red], plan is [bold cyan]{key_plan}[/bold cyan], [bold red]manual verification required[/bold red]')
        return [key, True, key_plan]
    except:
        log.info(f'[bold blue]{key}[/bold blue] is [bold red]INVALID[/bold red] as [bold yellow]SHODAN KEY[/bold yellow]')
        shodan_invalid_keys.append(key)
        return [key, False]
