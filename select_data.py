import re
import io

from utils import *
from model import Model
from user_input import UserInput


def morph(specs: str):
    matched = re.search(r"~([a-z\-]+)", specs)
    return matched.group(1) if matched else None


class SelectData:
    class Field:
        sort_symbol = "^"
        search_symbol = "?"

        def __init__(self, name: str, alias: str, specs: tuple[str, str]):
            self.name = name
            self.alias = alias
            self.specs, qualities = specs if specs else (None, None)
            self.sortable = self.sort_symbol in qualities if qualities else None
            self.searchable = self.search_symbol in qualities if qualities else None

    def __init__(self, spec: str, model: Model):
        self.model_table, self.primary_key = [s.strip() for s in spec.split(";")]
        self.output = io.StringIO()
        self.tables = {}
        self.fields = None  # track the fields in current table, Haribol
        # self.model = model
        self.ui = UserInput(model)

    def assignSpecs(self, field_name: str, back_name: str, specs: str):
        morph_specs = None
        qualities = None  # search / sort
        specs = [s.strip() for s in (specs.split(",") if specs else [])]
        for spec in specs:
            matched = re.match(r"[ ]*(i|#|\$)[ ]*\((.*)\)(.*)", spec)
            if matched:
                match matched.group(1):
                    case "i":
                        self.ui.appendField(
                            camel_case(field_name),
                            back_name,
                            matched.group(2),
                            matched.group(3),
                        )
                    case "#":
                        morph_specs = morph(matched.group(2))
                        qualities = matched.group(3)
                    case "$":
                        self.ui.assign_foreign_key(camel_case(field_name), back_name)
                    case _:
                        warn("Unheard specs type, Haribol")
        return (morph_specs, qualities)

    def append(self, line: str):
        if not (line := line.strip()):
            return
        matched = re.match("\\*{2}[ ]*(.*?)[ ]*\\*{2}", line)
        if matched:
            self.fields = self.tables.setdefault(matched.group(1), [])
        else:
            matched = re.match(
                f"({identifier})(?:[ ]+as[ ]+({identifier}))?(?:[ ]*:(.*))?", line
            )
            if not matched:
                error("DB field name spec is improper, Haribol!")

            if self.fields is None:
                error("No table name in specs, Haribol!")

            name = matched.group(1)
            alias = matched.group(2)
            self.fields.append(
                self.Field(
                    name,
                    alias,
                    self.assignSpecs(alias if alias else name, name, matched.group(3)),
                )
            )

    def ensure_primary_key_pagination(self):
        fields = self.tables.setdefault(self.model_table, [])
        if not find(lambda x: x.name == self.primary_key, fields):
            self.tables[self.model_table].append(
                self.Field(self.primary_key, None, None)
            )
            print("included, Haribol!")

    def generate_select_data(self):
        print(
            f"*** SelectData: {self.model_table}, {self.primary_key} ***",
            file=self.output,
        )
        self.ensure_primary_key_pagination()
        for table in self.tables:
            for field in self.tables[table]:
                alias = f" as {field.alias}" if field.alias else ""
                print(f"'{table}.{field.name}{alias}',", file=self.output)
        print("******\n", file=self.output)

    def generate_pagination(self):
        print("*** Paginate (SelectData) ***", file=self.output)
        for table in self.tables:
            for field in self.tables[table]:
                alias = field.alias if field.alias else field.name
                print(
                    (
                        "'id'"
                        if table == self.model_table and field.name == self.primary_key
                        else f"'{camel_case(alias)}'"
                    ),
                    "=>",
                    end=" ",
                    file=self.output,
                )
                match field.specs:
                    case None:
                        print(f"$item->{alias},", file=self.output)
                    case "file":
                        print(f"Storage::url($item->{alias}),", file=self.output)
                    case "date-only":
                        print(
                            f"Utils::formatDateJs($item->{alias}, DateFormatJs::OnlyDate),",
                            file=self.output,
                        )
                    case "date-time":
                        print(
                            f"Utils::formatDateJs($item->{alias}, DateFormatJs::DateTime),",
                            file=self.output,
                        )
                    case _:
                        print(file=self.output)
                        warn("Unknown transformation type, Haribol", field.specs)
        print("******\n", file=self.output)

    def generate_search_clause(self):
        print("*** Search clause (Select Data) ***", file=self.output)
        for table in self.tables.items():
            for field in table[1]:
                if field.searchable:
                    print(f"'{table[0]}.{field.name}',", file=self.output)
        print("******\n", file=self.output)

    def generate(self):
        self.generate_select_data()
        self.generate_pagination()
        self.generate_search_clause()
        ui_code = self.ui.generate()
        if ui_code:
            self.output.write(ui_code.getvalue())
        return self.output
