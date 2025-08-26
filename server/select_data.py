import re
import io

import utils
import sections
import sql_utils
from model import Model
from user_input import UserInput
from routes import Routes
from validation_error import ValidationError


class SelectData:
    class Field:
        search_symbol = "?"

        def __init__(
            self, name: str, alias: str, specs: tuple[str, str, bool, str, bool]
        ):
            self.name = name
            self.alias = alias
            self.specs, qualities, self.fillable, self.foreign, self.outputted = (
                specs if specs else (None, None, False, None, False)
            )
            # self.sortable = (
            #     UserInput.Field.sort_symbol in qualities if qualities else None
            # )
            # self.sortOrdinal = (
            #     (int(m.group(1)) if m.group(1) else None)
            #     if qualities and (m := re.search(r"\^([0-9]*)", qualities))
            #     else None
            # )
            self.searchable = self.search_symbol in qualities if qualities else None

        def camelCasedNameForUi(self):
            return utils.camel_case(self.alias if self.alias else self.name)

    def cntxt_id(self):
        return utils.camel_case(self.foreign_key)

    def __parse_foreign_specs(self, foreign_specs: list[str]):
        if not foreign_specs:
            self.cntxt_table, self.foreign_key = (None, None)
            return
        self.cntxt_table, self.foreign_key = [
            s.strip() for s in foreign_specs[0].split(";")
        ]
        sql_utils.check_table(self.cntxt_table)
        sql_utils.check_column(self.cntxt_table, self.foreign_key)
        self.ui.assign_foreign_key(
            self.cntxt_id(), self.foreign_key, self.model.cntxt_name
        )
        return

    def __init__(self, specs: str):
        specs = specs.split(",")
        native_specs = specs[0]
        foreign_specs = specs[1:]
        self.model_table, self.primary_key = [
            s.strip() for s in native_specs.split(";")
        ]
        if not self.model_table:
            utils.error("Model table name is missing, Haribol!")
        if not self.primary_key:
            utils.error("Primary key name is missing, Haribol!")

        self.model: Model = sections.ix("Model")
        self.model.primary_key = self.primary_key
        self.ui = UserInput(self.model_table)
        self.__parse_foreign_specs(foreign_specs)
        self.output = io.StringIO()
        self.tables: dict[str, list[SelectData.Field]] = {}
        self.cur_table: str = (
            None  # track the table whose fields are being read, Haribol
        )
        self.fields: list[SelectData.Field] = (
            None  # track the fields in current table, Haribol
        )
        self.routes: Routes = sections.ix("Routes")

    def parse_specs(
        self,
        field_name: str,
        back_name: str,
        specs: str,
    ):
        morph_specs = None
        qualities = None  # search / sort, Haribol
        fillable = False  # mass assignable, Haribol
        foreign = None  # specifies foreign table, Haribol
        outputted = False  # is value displayed in the UI?
        specs = [s.strip() for s in (specs.split(",") if specs else [])]
        for spec in specs:
            matched = re.match(r"[ ]*(i|#[0-9]+|\$|~)[ ]*\((.*)\)(.*)", spec)
            if matched:
                match matched.group(1):
                    case "i":
                        fillable = True
                        self.ui.append_field(
                            utils.camel_case(field_name),
                            back_name,
                            matched.group(2),
                            matched.group(3),
                        )
                    case "~":
                        morph_specs = matched.group(2)
                    case "$":
                        fillable = True
                        foreign = matched.group(2)
                        self.ui.append_grid_source(
                            utils.camel_case(field_name), utils.camel_case(foreign)
                        )
                    case _:
                        spec_type = matched.group(1)
                        if spec_type[0] == "#":
                            outputted = True
                            qualities = matched.group(3)
                            self.ui.append_grid_column(
                                int(spec_type[1:]),
                                utils.camel_case(field_name),
                                matched.group(2),
                                qualities,
                            )
                        else:
                            utils.warn("Unheard specs type, Haribol")
        if fillable:
            self.model.append_field(back_name)
        return (morph_specs, qualities, fillable, foreign, outputted)

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
                    ),
                )
            )

    def ensure_primary_key_pagination(self):
        fields = self.tables.setdefault(self.model_table, [])
        if not utils.find(lambda x: x.name == self.primary_key, fields):
            fields.append(self.Field(self.primary_key, None, None))
            print("Auto-included primary key, Haribol!")

    def find_foreign_table(self, key):
        for table, fields in self.tables.items():
            if table == self.model_table:
                continue
            for field in fields:
                if (
                    field.alias
                    and field.alias == key
                    or not field.alias
                    and field.name == key
                ):
                    return (table, field.name)
        return (None, None)

    def generate_join_clause(self):
        output = io.StringIO()
        for field in self.tables[self.model_table]:
            if field.foreign:
                foreign_table, ref_key = self.find_foreign_table(field.foreign)
                if not foreign_table:  # equivalent to: not ref_key
                    raise ValidationError(
                        "Failed to find referred column, Haribol!",
                        self.model_table,
                        field.name,
                    )
                print(
                    f"->join('{foreign_table}', '{self.model_table}.{field.name}', '=', '{foreign_table}.{ref_key}')",
                    file=output,
                )
        print(file=output)
        return output

    def generate_select_data(self):
        output = io.StringIO()
        self.ensure_primary_key_pagination()

        if self.foreign_key:
            self.model.append_field(self.foreign_key)

        for table in self.tables:
            for field in self.tables[table]:
                alias = f" as {field.alias}" if field.alias else ""
                if not field.foreign:
                    print(f"'{table}.{field.name}{alias}',", file=output)
        return output

    def generate_pagination_data(self):
        def print_field(name):
            print(
                f"'{name}'",
                "=>",
                end=" ",
                file=output,
            )
            match field.specs:
                case None:
                    print(f"$item->{alias},", file=output)
                case "file":
                    print(
                        f"Utils::asset($item->{alias}),",
                        file=output,
                    )
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

        output = io.StringIO()
        for table in self.tables:
            for field in self.tables[table]:
                # if field.foreign:
                #     continue
                alias = field.alias if field.alias else field.name
                if table == self.model_table and field.name == self.primary_key:
                    if field.fillable and field.name == "id":
                        utils.error(
                            "Inputting primary key field 'id' is not supported, Haribol!"
                        )
                    print_field("id")
                if (
                    field.fillable
                    or field.outputted
                    or self.ui.refers(utils.camel_case(alias))
                ):
                    print_field(utils.camel_case(alias))
        return output

    def generate_log_access(self):
        output = io.StringIO()
        print(
            f"LogAccessHelper::log({self.model.name}::class, $searchKey);", file=output
        )
        return output

    def generate_search_clause(self):
        output = io.StringIO()
        for table in self.tables.items():
            for field in table[1]:
                if field.searchable:
                    print(f"'{table[0]}.{field.name}',", file=output)
        return output

    def default_sort_field(self):
        for table in self.tables:
            for field in self.tables[table]:
                if self.ui.sort_ordinal(field.camelCasedNameForUi()) == 1:
                    return f"'{table}.{field.name}'"
        utils.warn('No field has been made as the default sort field, Haribol')
        return f"'{self.model_table}.{self.primary_key}'"

    def generate_declare_cntxt(self):
        output = io.StringIO()
        if self.cntxt_table:
            print(f"\nuse App\\Models\\{self.model.cntxt_name};", file=output)
        return output

    def generate_declare_cntxt_trait(self):
        output = io.StringIO()
        if self.cntxt_table:
            print(f"use App\\Traits\\{self.model.cntxt_name}Context;\n", file=output)
        return output

    def generate_use_cntxt_trait(self):
        output = io.StringIO()
        if self.cntxt_table:
            print(f"\nuse {self.model.cntxt_name}Context;\n", file=output)
        return output

    def generate_sort_by_id(self):
        output = io.StringIO()
        if self.primary_key != "id":
            print(
                f"""
                if ($sortField === 'id') {{
                    $sortField = '{self.primary_key}';
                }}
                """,
                file=output,
            )
        return output

    funcs = [
        ("*** Context Declaration ***", generate_declare_cntxt),
        ("*** Context Trait Declaration ***", generate_declare_cntxt_trait),
        ("*** Context Trait Usage ***", generate_use_cntxt_trait),
        ("*** Sort by id column (SelectData) ***", generate_sort_by_id),
        ("*** Join clause (SelectData) ***", generate_join_clause),
        ("*** SelectData columns ***", generate_select_data),
        ("*** Log Access (SelectData) ***", generate_log_access),
        ("*** Search clause (Select Data) ***", generate_search_clause),
        ("*** Paginate (SelectData) ***", generate_pagination_data),
    ]

    def generate(self):
        for func in self.funcs:
            print(func[0], file=self.output)
            try:
                self.output.write(func[1](self, *func[2:]).getvalue())
            except Exception as ex:
                utils.warn(ex)
            print("******\n", file=self.output)
        ui_code = self.ui.generate()
        if ui_code:
            self.output.write(ui_code.getvalue())
        return self.output

    def has_field(self, name: str):
        for table, fields in self.tables.items():
            for field in fields:
                field_name = field.alias if field.alias else field.name
                if field_name == name:
                    return table
        return None

    def declare_cntxt_id_variable(self):
        # output = io.StringIO()
        if not self.cntxt_table:  # same as checking 'not self.foreign_key', Haribol
            return ""
        return f"int ${self.cntxt_id()}"
        # return output

    def cntxt_filter(self):
        if not self.cntxt_table:  # same as checking 'not self.foreign_key', Haribol
            return ""
        return f"\n->where('{self.model_table}.{self.foreign_key}', ${self.cntxt_id()})"

    def menu_route_name(self):
        return self.routes.cntxt_name if self.routes.cntxt_name else self.routes.name

    def generate_model_props(self):
        output = io.StringIO()
        arg = (
            "" if not self.cntxt_table else f"${self.cntxt_id()}"
        )  # same as checking 'not self.foreign_key', Haribol
        print(
            f"'{self.ui.model_props}' => {self.model.name}Helper::paginate({arg}),",
            file=output,
        )
        return output

    def cntxt_route_param_store(self):
        if not self.cntxt_table:
            return ""
        return f"""[
            '{utils.first_char_lower(self.model.cntxt_name)}' => request('{self.cntxt_id()}')
        ]"""

    def cntxt_route_param_update(self):
        if not self.cntxt_table:
            return ""
        return f"""[
            '{utils.first_char_lower(self.model.cntxt_name)}' => {self.ui.model_varname()}->{self.foreign_key}
        ]"""

    def hydrateHelper(self):
        template = open("templates/ModelHelper.txt")
        model_helper = f"{self.model.name}Helper"
        output = open(f"output/{model_helper}.php", "wt")
        repo = {
            "model": self.model.name,
            "declare_cntxt_trait": self.generate_declare_cntxt_trait().getvalue(),
            "use_cntxt_trait": self.generate_use_cntxt_trait().getvalue(),
            "model_helper": model_helper,
            "declare_cntxt_var": self.declare_cntxt_id_variable(),
            "cntxt_var": f"${self.cntxt_id()}" if self.cntxt_table else "",
            "default_sort_field": self.default_sort_field(),
            "join_clause": self.generate_join_clause().getvalue(),
            "if_sort_by_id": self.generate_sort_by_id().getvalue(),
            "select_data": self.generate_select_data().getvalue(),
            "cntxt_filter": self.cntxt_filter(),
            "log_access": self.generate_log_access().getvalue(),
            "search_clause": self.generate_search_clause().getvalue(),
            "pagination_data": self.generate_pagination_data().getvalue(),
            "store_data": self.ui.generate_store_data().getvalue(),
            "update_data": self.ui.generate_update_data().getvalue(),
            "model_varname": self.ui.model_varname(),
        }
        while line := template.readline():
            hydrated = utils.hydrate(line, repo)
            print(hydrated, end="", file=output)
        template.close()
        output.close()
        self.ui.hydrate()

    def hydrateController(self):
        model_helper = f"{self.model.name}Helper"
        template = open("templates/ModelController.txt")
        model_controller = f"{self.model.name}Controller"
        output = open(f"output/{model_controller}.php", "wt")
        repo = {
            "model": self.model.name,
            "declare_cntxt": self.generate_declare_cntxt().getvalue(),
            "model_helper": model_helper,
            "declare_cntxt_var": self.declare_cntxt_id_variable(),
            "model_view_folder": utils.first_char_upper(
                utils.title_case(self.model_table)
            ),
            "menu_route": f", '{self.menu_route_name()}'",
            "model_props": self.generate_model_props().getvalue(),
            "controller_props": self.ui.generate_controller_props().getvalue(),
            "validation_fields": self.ui.generate_controller_validation().getvalue(),
            "model_varname": self.ui.model_varname(),
            "cntxt_request": (
                f"request('{self.cntxt_id()}')" if self.foreign_key else ""
            ),
            "model_route": f"'{self.routes.name}'",
            "cntxt_route_param_store": self.cntxt_route_param_store(),
            "cntxt_route_param_update": self.cntxt_route_param_update(),
        }
        while line := template.readline():
            hydrated = utils.hydrate(line, repo)
            print(hydrated, end="", file=output)
        template.close()
        output.close()

    def hydrate(self):
        self.hydrateHelper()
        self.hydrateController()
        self.ui.hydrate()

    def jsonify(self):
        return {
            "entityTableName": self.model_table,
            "entityTablePrimaryKey": self.primary_key,
            "cntxtTableName": self.cntxt_table,
            "cntxtTablePrimaryKey": self.foreign_key,
            "tables": [
                {
                    "name": table,
                    "fields": [
                        {
                            "name": field.name,
                            "alias": field.alias,
                            "morphSpecs": field.specs,
                            "foreign": field.foreign,
                            "fillable": field.fillable,
                            "inputSpecs": (
                                self.ui.input_specs(field.camelCasedNameForUi())
                                if field.fillable
                                else None
                            ),
                            "outputted": field.outputted,
                            "outputSpecs": (
                                self.ui.output_specs(field.camelCasedNameForUi(), field.searchable)
                                if field.outputted
                                else None
                            ),
                        }
                        for field in fields
                    ],
                }
                for table, fields in self.tables.items()
            ],
        }
