from colorama import Fore


class SystemMessages:

    def log(self, message: str) -> None:
        print(Fore.MAGENTA + f'\n{message}' + Fore.RESET)

    def success(self, message: str) -> None:
        print(Fore.GREEN + f'\n{message}' + Fore.RESET)

    def error(self, message: str) -> None:
        print(Fore.RED + f'\n{message}' + Fore.RESET)
