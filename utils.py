from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

def printError(msg):
    print(f"{Fore.RED}{msg}{Style.RESET_ALL}!")