from typing import List
from typing import Any


def read_json_file(file: str) -> Any:
    import json

    data_path = resource_path(file + '.json')
    with open(data_path, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)

    return data


def tuple_list_to_str_list(data: List[tuple]) -> List[Any]:
    if len(data) > 0:
        string_list = [
            f'{arg[0]} - {arg[1]} - {arg[2]} - {arg[3]}' for arg in data]

        return string_list

    return []


def access_dir(path_dir: str, filename: str) -> str:
    import os

    if not os.path.exists(os.getcwd() + '\\' + path_dir):
        os.makedirs(os.getcwd() + '\\' + path_dir)

    path_dir = os.path.join(os.getcwd(), path_dir)
    save_path = os.path.join(path_dir, filename)

    return save_path


def delete_file_from_path(file_path: str) -> None:
    import os
    os.remove(file_path)


def get_all_files_in_download_dir() -> List[str]:
    import os
    files_list = os.listdir(os.path.join(os.getcwd(), 'docs/downloads'))

    return files_list


def check_if_data_dont_have_special_character(data: str) -> str:
    import re
    check = re.sub(r'[<>:"/\\|?*]', "_", data)

    return check


def convert_int_to_brl_currency(value: int) -> str:
    value = value / 100
    new_value = '{:,.2f}'.format(value).replace(
        ',', 'X').replace('.', ',').replace('X', '.')

    return new_value


def resource_path(relative_path: str) -> str:
    import os
    import sys

    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
