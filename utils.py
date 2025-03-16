import re

# pip install colorful
import colorful as cf

identifier = "[a-zA-Z0-9_]+"


def note(mesg, *args):
    colon = ":" if args else ""
    print(f"{cf.yellow}{mesg}{colon}", *args, cf.reset)


def warn(mesg, *args):
    colon = ":" if args else ""
    print(f"{cf.coral}{mesg}{colon}", *args, cf.reset)


def error(mesg, *args, halt=True):
    colon = ":" if args else ""
    print(f"{cf.red}{mesg}{colon}", *args, cf.reset)
    if halt:
        exit()


def nullishIndex(ar: list, ix: int):
    try:
        return ar[ix]
    except IndexError:
        return None


def camel_case(name: str):
    return re.sub("_(.)", lambda v: v.group(1).upper(), name)


def find(pred, elems: iter):
    return next((elem for elem in elems if pred(elem)), None)


def strip_last_newline(s: str):
    return s[:-1] if s.endswith('\n') else s


def hydrate(line: str, args: dict):
    if not args:
        return line
    
    def replace(match: re.Match):
        try:
            return strip_last_newline(args[match.group(1)])
        except:
            warn("Not hydrated:", match.group(0))
            return match.group(0)

    return re.sub("@@@[ ]*([a-z_0-9]+)[ ]*@@@", replace, line)
