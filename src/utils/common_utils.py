import json
from typing import List


def read_json_file(file: str):
    with open(file + '.json', 'r') as json_file:
        data = json.load(json_file)

    return data


def tuple_list_to_str_list(data: List[tuple]):
    if len(data) > 0:
        string_list = [f'{arg[0]} - {arg[1]}' for arg in data]

        return string_list
