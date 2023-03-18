from other.style import bold_green, bold_red, bold_cyan, bold_yellow, reset
from censys.search.v2.api import CensysSearchAPIv2
import json

censys_valid_keys = []
censys_invalid_keys = []


def check(id_and_secret: str):
    id_and_secret_list = id_and_secret.split(':')
    try:
        allowance = CensysSearchAPIv2(api_id=id_and_secret_list[0], api_secret=id_and_secret_list[1]).quota()
        json_acceptable = str(allowance).replace("'", '"')
        allowance = json.loads(json_acceptable)['allowance']
        print(
            f'{bold_cyan}ID:{reset} {id_and_secret_list[0]} {bold_cyan}SECRET:{reset} {id_and_secret_list[1]} is a {bold_green}VALID{reset} {bold_yellow}CENSYS KEY{reset} and has allowance of {bold_cyan}{allowance}{reset}')
        return [id_and_secret, True, allowance]
    except:
        print(f'{id_and_secret} is {bold_red}INVALID{reset} as {bold_yellow}CENSYS KEY{reset}')
        return [id_and_secret, False]
