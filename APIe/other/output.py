from csv import writer
from rich import print


def print_title(app_name: str, status: str = ''):
    status = f' {status}' if status != '' else status
    print(f'\n[bold blue][+] Valid {app_name}[/][bold green]{status}[/] [bold blue]Keys[/]')


def print_keys(list_of_keys: list, keep_status: bool = True):
    if keep_status:
        for key in list_of_keys: print(f'[bold]{key[0]}[/] [cyan]{key[1]}[/]')
    else:
        for key in list_of_keys: print(f'[bold]{key[0]}[/]')


def print_total(list_of_key_lists: list, is_valid: bool = True, app_name: str = ''):
    total = 0
    for key_list in list_of_key_lists:
        total += len(key_list)
    valid = ['Valid', 'green'] if is_valid else ['Invalid', 'red']
    print(f'[bold blue]{app_name}[/] {valid[0]} Keys: [bold {valid[1]}]{total}[/]')


def open_csv_file(name: str = 'output'):
    name = f'{name}.csv' if 'csv' not in name else name
    with open(name, 'w') as output:
        writer(output).writerow(['app_name', 'credentials', 'status'])
        return name


def write_to_csv(app_name: str, credentials_list: list, file_name: str):
    with open(file_name, 'a') as output:
        for key in credentials_list:
            writer(output).writerow([app_name, key[0], key[1]])
