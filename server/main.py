import re
import json
import utils
import sections

from select_data import SelectData
from model import Model
from routes import Routes
import db_inspect

cur_sect = None


def build_section(line: str):
    # global cur_sect, model_section, select_data_section
    cur_sect = sections.last_set()
    matched = re.match("\\*{3}[ ]*(.*?)(?::[ ]*(.*?))?[ ]*\\*{3}", line)
    if matched:
        match (matched.group(1)):
            case "SelectData":
                sections.set(SelectData(matched.group(2)))
            case "Model":
                sections.set(Model(matched.group(2)))
            case "Routes":
                sections.set(Routes(matched.group(2)))
            case _:
                print("section: <", matched.group(1), ">", sep="")
                return
    elif cur_sect:
        cur_sect.append(line)


def read_sections():
    spec = open("templates/input.spec")
    try:
        while line := spec.readline():
            line = line.strip()
            if not line or line.startswith("#"):  # comment, Haribol
                continue
            build_section(line)
    finally:
        spec.close()


def list_columns(name, cntxt_name):
    with open("sql.json") as f:
        db_config = json.loads(f.read())["connect"]
        return db_inspect.get_columns_with_foreign_keys(
            db_config,
            name,
            [cntxt_name],
            ["created_by", "created_on", "modified_by", "modified_on"],
        )


def generate():
    output = open(
        "output/output.txt",
        "wt",
    )
    if gen := sections.ix("SelectData").generate():
        output.write(gen.getvalue())
    if gen := sections.ix("Model").generate():
        output.write(gen.getvalue())
    utils.diagnostics()


def hydrate():
    for section in sections.iterator():
        section.hydrate()


def save(json):
    model = json["model"]
    sections.set(Model(f"{model['name']}, {model['cntxtName']}"))
