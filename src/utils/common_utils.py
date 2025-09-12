from typing import List
from typing import Callable, Awaitable, Any


def read_json_file(file: str) -> Any:
    import json
    with open(file + '.json', 'r') as json_file:
        data = json.load(json_file)

    return data


def tuple_list_to_str_list(data: List[tuple]) -> List[Any]:
    if len(data) > 0:
        string_list = [
            f'{arg[0]} - {arg[1]} - {arg[2]} - {arg[3]}' for arg in data]

        return string_list

    return []


class SystemMessages:
    from colorama import Fore

    def log(self, message: str) -> Any:
        print(self.Fore.MAGENTA + message + self.Fore.RESET)

    def success(self, message: str) -> Any:
        print(self.Fore.GREEN + message + self.Fore.RESET)

    def error(self, message: str) -> Any:
        print(self.Fore.RED + message + self.Fore.RESET)


def access_download_dir(filename: str) -> str:
    import os
    path_dir = os.path.join(os.getcwd(), 'docs/downloads')
    save_path = os.path.join(path_dir, filename)

    return save_path


def check_if_data_dont_have_special_character(data: str) -> str:
    import re
    check = re.sub(r'[<>:"/\\|?*]', "_", data)

    return check


class RetryExecuter:
    def __init__(self):
        self.attempts = 3
        self.exception = Exception

    async def run(self, func: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any:
        from src.utils.common_utils import SystemMessages

        attempts = self.attempts
        while attempts > 0:
            try:
                return await func(*args, **kwargs)
            except self.exception as err:
                attempts -= 1
                if attempts == 0:
                    SystemMessages().error(f'RetryExecuter -> {str(err)}')
                    raise err
