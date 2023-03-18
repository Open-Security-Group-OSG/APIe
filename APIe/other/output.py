from csv import writer


def open_csv_file(name: str = 'output'):
    name = f'{name}.csv' if 'csv' not in name else name
    with open(name, 'w') as output:
        writer(output).writerow(['app_name', 'credentials', 'status'])
        return name


def write_to_csv(app_name: str, credentials_list: list, file_name: str):
    with open(file_name, 'a') as output:
        for key in credentials_list:
            writer(output).writerow([app_name, key[0], key[1]])
