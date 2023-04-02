from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printError(msg):
    print(f"{msg} {Fore.RED}color{Style.RESET_ALL}!")