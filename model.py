import re
import io

from utils import *


class Model:
    def __init__(self, spec: str):
        self.lines = []
        self.fields = []
        self.name = spec.strip()
        self.output = io.StringIO()

    def append(self, line):
        self.lines.append(line)

    def append_field(self, field: str):
        self.fields.append(field)

    def generate_fillable(self):
        output = io.StringIO()
        for field in self.fields:
            matched = re.match(f"[ ]*({identifier})[ ]*", field)
            if matched:
                print(f"'{matched.group(1)}',", file=output)
        return output

    def generate(self):
        print("*** Model: fillable ***", file=self.output)
        self.output.write(self.generate_fillable().getvalue())
        print("******\n", file=self.output)
        return self.output

    def hydrate(self):
        file = open("templates/model.txt")
        while line := file.readline():
            print(
                hydrate(
                    line,
                    {
                        "1": self.name,
                        "3": self.generate_fillable().getvalue()
                    },
                ),
                end="",
            )
        file.close()
