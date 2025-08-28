import json

with open("config.json") as cfg_file:
    config = json.loads(cfg_file.read())

connect = config["connect"]
model = config["model"]


def lower_each(xt):
    return map(lambda x: x.lower(), xt)


def upper_each(xt):
    return map(lambda x: x.upper(), xt)


skip_reflect = (
    list(lower_each(config["model"].values()))
    + list(upper_each(config["model"].values()))
    + list(lower_each(config["reflect"]["skip"]))
    + list(upper_each(config["reflect"]["skip"]))
)
