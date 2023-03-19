from requests import get
from other.logger import log
from other.output import print_title, print_keys

binaryedge_free_keys = []
binaryedge_starter_keys = []
binaryedge_business_keys = []
binaryedge_enterprise_keys = []


def check(key: str):
    try:
        key_plan = get('https://api.binaryedge.io/v2/user/subscription', headers={'X-Key': f'{key}'}).json()['subscription']['name']
        log.info(f'[bold blue]{key}[/] is a [bold green]VALID[/] [bold yellow]BINARYEDGE KEY[/] and plan is [bold cyan]{str(key_plan).upper()}[/]')

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
                log.warning(f'[bold yellow][ATTENTION][/] Weird key detected - [bold red]{key}[/], plan is [bold cyan]{key_plan}[/], [bold red]manual verification required[/]')
        return [key, True, key_plan]
    except:
        log.info(f'[bold blue]{key}[/] is [bold red]INVALID[/] as [bold yellow]BINARYEDGE KEY[/]')
        binaryedge_invalid_keys.append(key)
        return [key, False]


def present():
    if binaryedge_free_keys:
        print_title('BinaryEdge', 'FREE')
        print_keys(binaryedge_free_keys, keep_status=False)
    if binaryedge_starter_keys:
        print_title('BinaryEdge', 'STARTER')
        print_keys(binaryedge_starter_keys, keep_status=False)
    if binaryedge_business_keys:
        print_title('BinaryEdge', 'BUSINESS')
        print_keys(binaryedge_business_keys, keep_status=False)
    if binaryedge_enterprise_keys:
        print_title('BinaryEdge', 'ENTERPRISE')
        print_keys(binaryedge_enterprise_keys, keep_status=False)
