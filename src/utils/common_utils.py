from typing import List


def read_json_file(file: str):
    import json
    with open(file + '.json', 'r') as json_file:
        data = json.load(json_file)

    return data


def tuple_list_to_str_list(data: List[tuple]):
    if len(data) > 0:
        string_list = [f'{arg[0]} - {arg[1]} - {arg[2]}' for arg in data]

        return string_list

    return []


class SystemMessages:
    from colorama import Fore

    def log(self, message: str):
        print(self.Fore.MAGENTA + message + self.Fore.RESET)

    def success(self, message: str):
        print(self.Fore.GREEN + message + self.Fore.RESET)

    def error(self, message: str):
        print(self.Fore.RED + message + self.Fore.RESET)


def access_download_dir(filename: str):
    import os
    path_dir = os.path.join(os.getcwd(), 'docs/downloads')
    save_path = os.path.join(path_dir, filename)

    return save_path


def check_if_data_dont_have_special_character(data: str):
    import re
    check = re.sub(r'[<>:"/\\|?*]', "_", data)

    return check
