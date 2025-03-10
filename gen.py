import re
import io

from utils import *
from select_data import SelectData
from model import Model

sections = []
cur_sect = None

model_section = None


def read_sections():
    global cur_sect
    spec = open("input.spec")
    while line := spec.readline():
        line = line.strip()
        if not line or line.startswith("#"):  # comment, Haribol
            continue
        matched = re.match("\\*{3}[ ]*(.*?)(?::[ ]*(.*?))?[ ]*\\*{3}", line)
        if matched:
            match (matched.group(1)):
                case "SelectData":
                    sections.append(SelectData(matched.group(2), model_section))
                case "Model":
                    sections.append(model_section := Model(matched.group(2)))
                case _:
                    print("section: <", matched.group(1), ">", sep="")
                    continue
            cur_sect = sections[-1]
        elif cur_sect:
            cur_sect.append(line)


read_sections()

output = open(
    "output.txt",
    "wt",
)
for section in sections:
    if gen := section.generate():
        output.write(gen.getvalue())
