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

    def generate(self):
        print("*** Model: fillable ***", file=self.output)
        for field in self.fields:
            matched = re.match(f"[ ]*({identifier})[ ]*", field)
            if matched:
                print(f"'{matched.group(1)}',", file=self.output)
        print("******\n", file=self.output)
        return self.output
