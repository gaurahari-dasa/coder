import json

with open("config.json") as cfg_file:
    config = json.loads(cfg_file.read())

connect = config["connect"]
model = config["model"]
skip_reflect = list(config["model"].values()) + config["reflect"]["skip"]
