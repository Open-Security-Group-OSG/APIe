invalid_keys = [[], []]


def invalid_clean_up(list_id: int):
    invalid_keys[list_id].clear()


def deduplicate_input(input_list: str):
    with open(input_list, 'r') as keys:
        deduplicated = list(dict.fromkeys(keys.readlines()))
        keys_list = []
        for key in deduplicated:
            keys_list.append(key.replace("\n", "").strip())

        return keys_list
