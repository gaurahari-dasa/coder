import re

#pip install colorful
import colorful as cf

identifier = '[a-zA-Z0-9_]+'

def note(mesg, *args):
    colon = ':' if args else ''
    print(f'{cf.green}{mesg}{colon}', *args, cf.reset)

def warn(mesg, *args):
    colon = ':' if args else ''
    print(f'{cf.red}{mesg}{colon}', *args, cf.reset)

def error(mesg, *args, halt=True):
    colon = ':' if args else ''
    print(f'{cf.yellow}{mesg}{colon}', *args, cf.reset)
    if halt:
        exit()

def nullishIndex(ar:list, ix:int):
    try:
        return ar[ix]
    except IndexError:
        return None

def camel_case(name:str):
    return re.sub('_(.)', lambda v: v.group(1).upper(), name)

def find(pred, elems:iter):
    return next((elem for elem in elems if pred(elem)), None)
