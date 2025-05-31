import re
import utils
import sections

from select_data import SelectData
from model import Model
from routes import Routes

cur_sect = None


def read_sections():
    global cur_sect, model_section, select_data_section
    spec = open("templates/input.spec")
    try:
        while line := spec.readline():
            line = line.strip()
            if not line or line.startswith("#"):  # comment, Haribol
                continue
            matched = re.match("\\*{3}[ ]*(.*?)(?::[ ]*(.*?))?[ ]*\\*{3}", line)
            if matched:
                match (matched.group(1)):
                    case "SelectData":
                        sections.set(SelectData(matched.group(2)), "SelectData")
                    case "Model":
                        sections.set(Model(matched.group(2)), "Model")
                    case "Routes":
                        sections.set(Routes(matched.group(2)), "Routes")
                    case _:
                        print("section: <", matched.group(1), ">", sep="")
                        continue
                cur_sect = sections.last_set()
            elif cur_sect:
                cur_sect.append(line)
    finally:
        spec.close()


# read_sections()


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


# for section in sections:
#     if gen := section.generate():
#         output.write(gen.getvalue())
