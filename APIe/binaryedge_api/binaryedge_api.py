from requests import get
from other.logger import log

binaryedge_free_keys = []
binaryedge_starter_keys = []
binaryedge_business_keys = []
binaryedge_enterprise_keys = []
binaryedge_invalid_keys = []


def check(key: str):
    try:
        key_plan = get('https://api.binaryedge.io/v2/user/subscription', headers={'X-Key': f'{key}'}).json()['subscription']['name']
        log.info(f'[bold blue]{key}[/bold blue] is a [bold green]VALID[/bold green] [bold yellow]BINARYEDGE KEY[/bold yellow] and plan is [bold cyan]{str(key_plan).upper()}[/bold cyan]')

        match key_plan.lower():
            case 'free':
                binaryedge_free_keys.append([key, key_plan])
            case 'starter':
                binaryedge_starter_keys.append([key, key_plan])
            case 'business':
                binaryedge_starter_keys.append([key, key_plan])
            case 'enterprise':
                binaryedge_enterprise_keys.append([key, key_plan])
            case _:
                binaryedge_invalid_keys.append(key)
                log.warning(f'[bold yellow][ATTENTION][/bold yellow] Weird key detected - [bold red]{key}[/bold red], plan is [bold cyan]{key_plan}[/bold cyan], [bold red]manual verification required[/bold red]')
        return [key, True, key_plan]
    except:
        log.info(f'[bold blue]{key}[/bold blue] is [bold red]INVALID[/bold red] as [bold yellow]BINARYEDGE KEY[/bold yellow]')
        binaryedge_invalid_keys.append(key)
        return [key, False]
