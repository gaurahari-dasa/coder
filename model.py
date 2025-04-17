import re
import io

import utils


class Model:
    def __init__(self, specs: str):
        self.lines = []
        self.fields = []
        specs = [s.strip() for s in specs.split(',')]
        self.name = specs[0]
        self.cntxt_name = utils.nullishIndex(specs, 1)
        self.output = io.StringIO()

    def append(self, line):
        self.lines.append(line)

    def append_field(self, field: str):
        self.fields.append(field)

    def generate_fillable(self):
        output = io.StringIO()
        for field in self.fields:
            matched = re.match(f"[ ]*({utils.identifier})[ ]*", field)
            if matched:
                print(f"'{matched.group(1)}',", file=output)
        return output

    def generate(self):
        print("*** Model: fillable ***", file=self.output)
        try:
            self.output.write(self.generate_fillable().getvalue())
        except Exception as ex:
            utils.warn(ex)
        print("******\n", file=self.output)
        return self.output

    def hydrate(self):
        template = open("templates/model.txt")
        output = open(f"output/{self.name}.php", "wt")
        repo = {
            "model": self.name,
            "primary_key": self.primary_key,
            "fillable": self.generate_fillable().getvalue(),
        }
        while line := template.readline():
            hydrated = utils.hydrate(line, repo)
            print(hydrated, end="", file=output)
        template.close()
        output.close()
