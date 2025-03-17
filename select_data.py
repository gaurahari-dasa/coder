import re
import io

import utils
import sql_utils
from model import Model
from user_input import UserInput


def morph(specs: str):
    matched = re.search(r"~([a-z\-]+)", specs)
    return matched.group(1) if matched else None


class SelectData:
    class Field:
        sort_symbol = "^"
        search_symbol = "?"

        def __init__(self, name: str, alias: str, specs: tuple[str, str, bool, str]):
            self.name = name
            self.alias = alias
            self.specs, qualities, self.fillable, self.foreign = (
                specs if specs else (None, None, False, None)
            )
            self.sortable = self.sort_symbol in qualities if qualities else None
            self.searchable = self.search_symbol in qualities if qualities else None

    def __init__(self, specs: str, model: Model):
        specs = specs.split(",")
        native_specs = specs[0]
        foreign_specs = specs[1:]
        self.model_table, self.primary_key = [
            s.strip() for s in native_specs.split(";")
        ]
        self.cntxt_table, self.foreign_key = (
            [s.strip() for s in foreign_specs[0].split(";")]
            if foreign_specs
            else (None, None)
        )
        self.output = io.StringIO()
        self.tables = {}
        self.cur_table = None  # track the table whose fields are being read, Haribol
        self.fields = None  # track the fields in current table, Haribol
        self.model = model
        model.primary_key = self.primary_key
        self.ui = UserInput(model, self.model_table)

    def parse_specs(
        self, field_name: str, back_name: str, specs: str, model_owned: bool
    ):
        morph_specs = None
        qualities = None  # search / sort, Haribol
        fillable = False  # mass assignable, Haribol
        foreign = None  # specifies foreign table, Haribol
        specs = [s.strip() for s in (specs.split(",") if specs else [])]
        for spec in specs:
            matched = re.match(r"[ ]*(i|#|\$)[ ]*\((.*)\)(.*)", spec)
            if matched:
                match matched.group(1):
                    case "i":
                        self.ui.append_field(
                            utils.camel_case(field_name),
                            back_name,
                            matched.group(2),
                            matched.group(3),
                        )
                    case "#":
                        morph_specs = morph(matched.group(2))
                        qualities = matched.group(3)
                    case "$":
                        foreign = matched.group(2)
                        if foreign == self.cntxt_table:
                            self.ui.assign_foreign_key(
                                utils.camel_case(field_name), back_name
                            )
                        # if not self.foreign_key:
                        #     # self.foreign_key = back_name
                        #     # self.cntxt_table = foreign
                        #     utils.error("No foreign table specs defined, Haribol")
                    case _:
                        utils.warn("Unheard specs type, Haribol")
                if matched.group(1) in ["i", "$"] and model_owned:
                    self.model.append_field(field_name)
                    fillable = True
        return (morph_specs, qualities, fillable, foreign)

    def append(self, line: str):
        if not (line := line.strip()):
            return
        matched = re.match("\\*{2}[ ]*(.*?)[ ]*\\*{2}", line)
        if matched:
            self.cur_table = matched.group(1)
            sql_utils.check_table(self.cur_table)
            self.fields = self.tables.setdefault(self.cur_table, [])
        else:
            matched = re.match(
                f"({utils.identifier})(?:[ ]+as[ ]+({utils.identifier}))?(?:[ ]*:(.*))?",
                line,
            )
            if not matched:
                utils.error("DB field name spec is improper, Haribol!")

            if self.fields is None:
                utils.error("No table name in specs, Haribol!")

            name = matched.group(1)
            sql_utils.check_column(self.cur_table, name)
            alias = matched.group(2)
            self.fields.append(
                self.Field(
                    name,
                    alias,
                    self.parse_specs(
                        alias if alias else name,
                        name,
                        matched.group(3),
                        self.cur_table == self.model_table,
                    ),
                )
            )

    def ensure_primary_key_pagination(self):
        fields = self.tables.setdefault(self.model_table, [])
        if not utils.find(lambda x: x.name == self.primary_key, fields):
            fields.append(self.Field(self.primary_key, None, None))
            print("Auto-included primary key, Haribol!")

    def foreign(self):
        fields = self.tables[self.model_table]
        return utils.find(lambda x: x.foreign == self.cntxt_table, fields)

    def ensure_foreign_key_cntxt(self):
        fields = self.tables.setdefault(self.model_table, [])
        if self.foreign_key and not utils.find(lambda x: x.foreign, fields):
            self.ui.assign_foreign_key(
                utils.camel_case(self.foreign_key), self.foreign_key
            )
            fields.append(
                self.Field(self.foreign_key, None, (None, None, True, self.foreign_key))
            )
            print("Auto-included foreign key, Haribol!")

    def generate_select_data(self):
        output = io.StringIO()
        self.ensure_primary_key_pagination()
        self.ensure_foreign_key_cntxt()
        for table in self.tables:
            for field in self.tables[table]:
                alias = f" as {field.alias}" if field.alias else ""
                if not field.foreign:
                    print(f"'{table}.{field.name}{alias}',", file=output)
        return output

    def generate_pagination(self):
        output = io.StringIO()
        for table in self.tables:
            for field in self.tables[table]:
                if field.foreign:
                    continue
                alias = field.alias if field.alias else field.name
                print(
                    (
                        "'id'"
                        if table == self.model_table and field.name == self.primary_key
                        else f"'{utils.camel_case(alias)}'"
                    ),
                    "=>",
                    end=" ",
                    file=output,
                )
                match field.specs:
                    case None:
                        print(f"$item->{alias},", file=output)
                    case "file":
                        print(f"Storage::url($item->{alias}),", file=output)
                    case "date-only":
                        print(
                            f"Utils::formatDateJs($item->{alias}, DateFormatJs::OnlyDate),",
                            file=output,
                        )
                    case "date-time":
                        print(
                            f"Utils::formatDateJs($item->{alias}, DateFormatJs::DateTime),",
                            file=output,
                        )
                    case _:
                        print(file=output)
                        utils.warn("Unknown transformation type, Haribol", field.specs)
        return output

    def generate_search_clause(self):
        output = io.StringIO()
        for table in self.tables.items():
            for field in table[1]:
                if field.searchable:
                    print(f"'{table[0]}.{field.name}',", file=output)
        return output

    def generate_sort_by_id(self):
        output = io.StringIO()
        id_field = utils.find(
            lambda x: x.name == self.primary_key, self.tables[self.model_table]
        )
        if id_field and id_field.sortable:
            print(
                rf"""
                if ($sortField === 'id') {{
                    $sortField = '{self.primary_key}'
                }}
                """,
                file=output,
            )
        return output

    funcs = [
        ("*** SelectData: model_table, primary_key ***", generate_select_data),
        ("*** Paginate (SelectData) ***", generate_pagination),
        ("*** Search clause (Select Data) ***", generate_search_clause),
        ("*** Sort by id column (SelectData) ***", generate_sort_by_id),
    ]

    def generate(self):
        for func in self.funcs:
            print(func[0], file=self.output)
            try:
                self.output.write(func[1](self).getvalue())
            except Exception as ex:
                utils.warn(ex)
            print("******\n", file=self.output)
        ui_code = self.ui.generate()
        if ui_code:
            self.output.write(ui_code.getvalue())
        return self.output

    def cntxt_filter(self):
        foreign = self.foreign()
        if not foreign == self.cntxt_table:
            return ""
        alias = foreign.alias if foreign.alias else foreign.name
        return f"\n->where('{self.model_table}.{foreign.name}', request('{utils.kebab_case(alias)}'))"

    def hydrate(self):
        template = open("templates/ModelHelper.txt")
        model_helper = f"{self.model.name}Helper"
        output = open(f"output/{model_helper}.php", "wt")
        while line := template.readline():
            print(
                utils.hydrate(
                    line,
                    {
                        "model": self.model.name,
                        "model_helper": model_helper,
                        "select_data": self.generate_select_data().getvalue(),
                        "cntxt_filter": self.cntxt_filter(),
                    },
                ),
                end="",
                file=output,
            )
        template.close()
        output.close()
