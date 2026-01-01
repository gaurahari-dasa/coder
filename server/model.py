import re
import io

import utils
import sections
import config


class Model:
    def __init__(self, specs: str):
        self.lines = []
        self.fields = []
        specs = [s.strip() for s in specs.split(",")]
        self.name = specs[0]
        self.cntxt_name = utils.nullishIndex(specs, 1)
        self.cntxt_var_name = utils.first_char_lower(self.cntxt_name)
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
        dates = []
        datetimes = []
        for field in fields.values():
            cast_type = None
            match field.type:
                case "checkbox":
                    cast_type = bools
                case "date":
                    cast_type = dates
                case "datetime-local":
                    cast_type = datetimes
            if cast_type != None:
                cast_type.append(field.base_name)

        bools_csv = "\n".join([f"'{b}' => 'boolean'," for b in bools])
        dates_csv = "\n".join([f"'{d}' => 'date:Y-m-d'," for d in dates])
        datetimes_csv = "\n".join([f"'{d}' => 'datetime'," for d in datetimes])

        print(
            f"""

    protected function casts(): array
    {{
        return [
            {bools_csv}{dates_csv}{datetimes_csv}
        ];
    }}""",
            file=output,
        )
        return output

    funcs = [
        ("*** Model: fillable ***", generate_fillable),
        ("*** Model: casts method ***", generate_casts_method),
    ]

    def generate_assign_table_keys(self):
        output = io.StringIO()
        key = config.model["created_at"]
        if key != "created_at":
            print(f"const CREATED_AT = '{key}';", file=output)
        key = config.model["updated_at"]
        if key != "updated_at":
            print(f"const UPDATED_AT = '{key}';", file=output)
        if self.primary_key != "id":
            if output.getvalue():
                print()
            print(f"protected $primaryKey = '{self.primary_key}';\n", file=output)
        return output

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
            "assign_table_keys": self.generate_assign_table_keys().getvalue(),
            "fillable": self.generate_fillable().getvalue(),
            "casts_method": self.generate_casts_method().getvalue(),
        }
        while line := template.readline():
            hydrated = utils.hydrate(line, repo)
            print(hydrated, end="", file=output)
        template.close()
        output.close()

    def jsonify(self):
        return {"name": self.name, "cntxtName": self.cntxt_name}
