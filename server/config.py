import json

with open("sql.json") as cfg_file:
    config = json.loads(cfg_file.read())

connect = config["connect"]
model = config["model"]
