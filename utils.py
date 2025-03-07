import re

#pip install colorama
import colorama

identifier = '[a-zA-Z0-9_]+'

colorama.init()

def printWarning(mesg, *args):
    print(f'{colorama.Fore.RED}{mesg}', args, colorama.Style.RESET_ALL)

def printError(mesg, *args):
    print(f'{colorama.Fore.YELLOW}{mesg}', args, colorama.Style.RESET_ALL)

def nullishIndex(ar:list, ix:int):
    try:
        return ar[ix]
    except IndexError:
        return None

def camel_case(name:str):
    return re.sub('_(.)', lambda v: v.group(1).upper(), name)
