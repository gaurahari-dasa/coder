import re
import io

from utils import *
from select_data import SelectData
from model import Model

sections = []
cur_sect = None

model_section = None
select_data_section = None


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
                        sections.append(
                            select_data_section := SelectData(
                                matched.group(2), model_section
                            )
                        )
                    case "Model":
                        sections.append(model_section := Model(matched.group(2)))
                    case _:
                        print("section: <", matched.group(1), ">", sep="")
                        continue
                cur_sect = sections[-1]
            elif cur_sect:
                cur_sect.append(line)
    finally:
        spec.close()


read_sections()

output = open(
    "output/output.txt",
    "wt",
)

if gen := select_data_section.generate():
    output.write(gen.getvalue())
if gen := model_section.generate():
    output.write(gen.getvalue())

model_section.hydrate()
select_data_section.hydrate()
# for section in sections:
#     if gen := section.generate():
#         output.write(gen.getvalue())
