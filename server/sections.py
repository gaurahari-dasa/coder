__sections = {}
__last_set = None


def set(sect, key: str = None):
    global __last_set
    __sections[key if key else type(sect).__name__] = __last_set = sect


def get(key: str):
    return __sections.get(key, None)


def ix(key: str):
    return __sections[key]


def last_set():
    return __last_set


def iterator():
    return iter(__sections.values())
