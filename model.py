import re
import io

from utils import *

class Model:
    def __init__(self):
        self.lines = []
        self.output = io.StringIO()

    def append(self, line):
        self.lines.append(line)

    def generate(self):
        print('*** Model: fillable ***', file=self.output)
        for line in self.lines:
            matched = re.match(f'[ ]*({identifier})', line)
            if matched:
                print(f"'{matched.group(1)}',", file=self.output)
        print('******', file=self.output)
        return self.output
