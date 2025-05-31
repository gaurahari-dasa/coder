import re
import io

# pip install colorful
import colorful as cf

identifier = "[a-zA-Z0-9_]+"
mesg_board = set()


def __write_message(color, mesg, *args):
    colon = ":" if args else ""
    buffer = io.StringIO()
    print(f"{color}{mesg}{colon}", *args, cf.reset, file=buffer)
    mesg_board.add(buffer.getvalue())
    buffer.close()


def note(mesg, *args):
    __write_message(cf.yellow, mesg, *args)


def warn(mesg, *args):
    __write_message(cf.coral, mesg, *args)


def error(mesg, *args):
    __write_message(cf.red, mesg, *args)
    diagnostics()
    exit()


def diagnostics():
    for mesg in mesg_board:
        print(mesg, end="")


def nullishIndex(ar: list, ix: int):
    try:
        return ar[ix]
    except IndexError:
        return None


def uncamel_case(name: str):
    return re.sub("([A-Z])", lambda v: "_" + v.group(1).lower(), name)


def camel_case(name: str):
    if re.search("[A-Z]", name):
        warn("Capital case characters found in string", name)
    return re.sub("_(.)", lambda v: v.group(1).upper(), name)


def kebab_case(name: str):
    return name.replace("_", "-")


def title_case(name: str):
    return re.sub("_(.)", lambda v: v.group(1).upper(), name)


def first_char_lower(name: str):
    return name[0].lower() + name[1:] if name else name


def first_char_upper(name: str):
    return name[0].upper() + name[1:] if name else name


def find(pred, elems: iter):
    return next((elem for elem in elems if pred(elem)), None)


def strip_last_newline(s: str):
    return s[:-1] if s.endswith("\n") else s


# variable used for noMatchValue attribute in FormSelect Vue component, Haribol
def no_match_var(match_value: str):
    return "edit" + first_char_upper(match_value)


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
