import re
import io

import utils
import sections


class Model:
    def __init__(self, specs: str):
        self.lines = []
        self.fields = []
        specs = [s.strip() for s in specs.split(",")]
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

    def generate_casts_method(self):
        output = io.StringIO()
        fields = sections.ix("SelectData").ui.fields
        bools = []
        for field in fields:
            if field.type == "checkbox":
                bools.append(field.base_name)
        if bools:
            bools_csv = "\n".join([f"'{b}' => 'boolean'," for b in bools])
            print(
                f"""

    protected function casts(): array
    {{
        return [
            {bools_csv}
        ];
    }}""",
                file=output,
            )
        return output

    funcs = [
        ("*** Model: fillable ***", generate_fillable),
        ("*** Model: casts method ***", generate_casts_method),
    ]

    def generate(self):
        for func in self.funcs:
            print(func[0], file=self.output)
            try:
                self.output.write(func[1](self, *func[2:]).getvalue())
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
            "casts_method": self.generate_casts_method().getvalue(),
        }
        while line := template.readline():
            hydrated = utils.hydrate(line, repo)
            print(hydrated, end="", file=output)
        template.close()
        output.close()
