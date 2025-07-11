import re
import io
from collections import namedtuple

import utils
import sections
from model import Model
from routes import Routes
from OrderedSet import OrderedSet


class UserInput:

    ForeignKey = namedtuple("ForeignKey", ["name", "base_name", "prop"])

    class Field:
        focus_symbol = "@"
        required_symbol = "*"

        # HTML select (FormSelect) control:
        # the following syntax is not yet implemented
        # id=languageId&value=name
        # id and value fields can be specified; if any one is missed out the default values are taken
        # If id is missed out, it's taken to be 'id'; if value is missed out, it's taken to be 'name'
        # the above syntax is reserved for future use
        def parse_bindings(bindings: str):
            bindings = [s.strip() for s in bindings.split("&")]
            result = {}
            for binding in bindings:
                param, value = [s.strip() for s in binding.split("=")]
                if ":" in param:
                    utils.error("Parameter alias is not yet supported!")
                result[param] = value

        def __init__(self, name: str, base_name: str, specs: str, qualities: str):
            self.name = name
            self.base_name = base_name  # name in database, Haribol
            specs = [s.strip() for s in (specs.split(";") if specs else specs)]
            self.type = specs[0]
            self.title = utils.nullishIndex(specs, 1)
            self.options = utils.nullishIndex(
                specs, 2
            )  # doubles up as the default value of checkbox, Haribol
            self.match_value: str = utils.nullishIndex(specs, 3)
            self.focus = self.focus_symbol in qualities
            self.required = self.required_symbol in qualities

    class GridColumn:
        sort_symbol = "^"

        def __init__(self, name: str, specs: str, qualities: str):
            self.name = name
            specs = [s.strip() for s in (specs.split(";") if specs else specs)]
            self.type = utils.nullishIndex(specs, 0)
            self.title = utils.nullishIndex(specs, 1)
            self.qualities = qualities

        def sortable(self):
            return self.sort_symbol in self.qualities

    def __init__(self, model_table: str):
        self.fields: dict[str, UserInput.Field] = {}
        self.no_match_vars = set()
        self.grid_sources = {}
        self.grid_columns = {}
        self.lookup_props = set()
        self.foreign_key = None
        self.model: Model = sections.ix("Model")
        self.model_table = model_table
        self.model_props = utils.camel_case(model_table)
        self.routes: Routes = sections.ix("Routes")
        self.vue_imports = OrderedSet()
        self.output = io.StringIO()

    def append_field(self, name, base_name, specs, qualities):
        self.fields[name] = self.Field(name, base_name, specs, qualities)

    def append_grid_source(self, name: str, grid_source: str):
        self.grid_sources[name] = grid_source

    def append_grid_column(self, index: int, name: str, spec: str, qualities: str):
        if index in self.grid_columns:
            utils.error("Grid column index is not unique, Haribol!")
        self.grid_columns[index] = self.GridColumn(name, spec, qualities)

    def assign_foreign_key(self, name, base_name, model_name):
        self.foreign_key = self.ForeignKey(
            name, base_name, utils.first_char_lower(model_name)
        )

    def generate_avatar_heading(self):
        output = io.StringIO()
        if self.foreign_key:
            self.vue_imports.add(
                "import AvatarHeading from '../../components/AvatarHeading.vue';"
            )
            print(
                f"""
            <AvatarHeading class="-mt-4 sm:-mt-6 lg:-mt-8" :user="{self.foreign_key.prop}" backLabel="Back to what (parent) ???"
                :backUrl="`${{baseUrl}}{self.routes.cntxt_url}`" />""",
                file=output,
            )
        return output

    def tackFocus(self, field):
        return " setFocus" if field.focus else ""

    def tackRequired(self, field):
        return " required" if field.required else ""

    def generate_typed_input(self, field: Field, output, type="text"):
        self.vue_imports.add("import FormInput from '../../components/FormInput.vue';")
        mx_len_attr = ""
        if field.type == "text":
            if not field.options:
                utils.warn(
                    "Missing maxLength option for FormInput component", field.name
                )
            else:
                mx_len_attr = f':maxLength="{field.options}" '
        print(
            f"""<FormInput type="{type}" class="mt-4" id="{field.name}" title="{field.title}"{self.tackFocus(field) + self.tackRequired(field)}
              {mx_len_attr}v-model="{self.form_obj}.{field.name}" :error="{self.form_obj}.errors.{field.name}" />""",
            file=output,
        )

    def generate_text_input(self, field: Field, output):
        self.generate_typed_input(field, output, type="text")

    def generate_email_input(self, field: Field, output):
        self.generate_typed_input(field, output, type="email")

    def generate_date_input(self, field: Field, output):
        self.generate_typed_input(field, output, type="date")

    def generate_select_input(self, field: Field, output):
        self.lookup_props.add(field.options)
        self.vue_imports.add(
            "import FormSelect from '../../components/FormSelect.vue';"
        )
        if not sections.ix("SelectData").has_field(
            utils.uncamel_case(field.match_value)
        ):
            utils.error("No source column for match_value, Haribol")
        no_match_var = utils.no_match_var(field.match_value)
        self.no_match_vars.add(no_match_var)
        no_match_attr = (
            f' :noMatchValue="{no_match_var}"' if self.form_obj == "editForm" else ""
        )
        print(
            f"""<FormSelect class="mt-4" id="{field.name}" title="{field.title}" :options="{field.options}"{self.tackFocus(field) + self.tackRequired(field)}
              v-model="{self.form_obj}.{field.name}"{no_match_attr} :error="{self.form_obj}.errors.{field.name}" />""",
            file=output,
        )

    def generate_checkbox_input(self, field: Field, output):
        self.vue_imports.add(
            "import FormCheckBox from '../../components/FormCheckBox.vue';"
        )
        print(
            f"""<FormCheckBox class="mt-4" id="{field.name}" title="{field.title}"
              :error="{self.form_obj}.errors.{field.name}" v-model="{self.form_obj}.{field.name}" />""",
            file=output,
        )

    def generate_file_upload(self, field: Field, output):
        self.vue_imports.add(
            "import FormFileUpload from '../../components/FormFileUpload.vue';"
        )
        print(
            f"""<FormFileUpload class="mt-4" id="{field.name}" title="{field.title}"{self.tackFocus(field) + self.tackRequired(field)}
              @pick="file => {self.form_obj}.{field.name} = file" :error="{self.form_obj}.errors.{field.name}" />""",
            file=output,
        )

    def generate_autocomplete(self, field: Field, output):
        self.lookup_props.add(field.options)
        self.vue_imports.add(
            "import FormAutoComplete from '../../components/FormAutoComplete.vue';"
        )
        print(
            f"""<FormAutoComplete class="mt-4" id="{field.name}" title="{field.title}" :options="{field.options}"{self.tackFocus(field) + self.tackRequired(field)}
              v-model="{self.form_obj}.{field.name}" :error="{self.form_obj}.errors.{field.name}" />""",
            file=output,
        )

    def generate_control(self, field: Field, output):
        match field.type:
            case "text":
                self.generate_text_input(field, output)
            case "email":
                self.generate_email_input(field, output)
            case "date":
                self.generate_date_input(field, output)
            case "select":
                self.generate_select_input(field, output)
            case "checkbox":
                self.generate_checkbox_input(field, output)
            case "file":
                self.generate_file_upload(field, output)
            case "auto":
                self.generate_autocomplete(field, output)
            case _:
                utils.warn("Unknown control, Haribol!", field.name, field.type)

    def generate_form_elements(self, form_type: str):
        output = io.StringIO()
        self.form_obj = form_type + "Form"
        for field in self.fields.values():
            self.generate_control(field, output)
        return output

    def grid_headings(self):
        return (
            "["
            + ", ".join([f"'{col.title}'" for col in self.grid_columns.values()])
            + "]"
        )

    def grid_fields(self):
        return (
            "["
            + ", ".join([f"'{col.name}'" for col in self.grid_columns.values()])
            + "]"
        )

    def grid_column_types(self):
        for col in self.grid_columns.values():
            self.vue_imports.add(
                f"import {col.type} from '../../components/{col.type}.vue';"
            )
        return (
            "[" + ", ".join([f"{col.type}" for col in self.grid_columns.values()]) + "]"
        )

    def grid_sortable_fields(self):
        return (
            "["
            + ", ".join(
                [
                    f"'{col.name}'"
                    for col in filter(
                        lambda v: v.sortable(),
                        self.grid_columns.values(),
                    )
                ]
            )
            + "]"
        )

    def generate_grid_parameters(self):
        output = io.StringIO()
        print("headings:", self.grid_headings(), file=output)
        print("column_types:", self.grid_column_types(), file=output)
        print("fields:", self.grid_fields(), file=output)
        print("sortable_fields:", self.grid_sortable_fields(), file=output)
        return output

    def generate_vue_imports(self):
        output = io.StringIO()
        print(
            "\n".join(self.vue_imports),
            file=output,
        )
        print(
            """import EntityCard from '../../components/EntityCard.vue';
import FormCancelButton from '../../components/FormCancelButton.vue';
import FormSubmitButton from '../../components/FormSubmitButton.vue';
import ToastMessage from '../../components/ToastMessage.vue';
import FormGuard from '../../components/FormGuard.vue';""",
            file=output,
        )
        return output

    def generate_blanked(self):
        output = io.StringIO()
        for field in self.fields.values():
            if field.type == "checkbox":
                if field.options:
                    value = field.options
                else:
                    value = "false"
                    utils.warn(
                        "Missing default value for checkbox type input; it will be set to false, Haribol!"
                    )
            else:
                value = "null"
            print(f"{field.name}: {value},", file=output)
        return output

    def generate_form(self, form_type: str):
        output = io.StringIO()
        if form_type == "add" and self.foreign_key:
            print("{", file=output)
            print(
                "...blanked,",
                file=output,
            )
            print(
                f"{self.foreign_key.name}: props.{self.foreign_key.name},",
                file=output,
            )
            print("}", file=output)
        else:
            print("blanked", file=output)
        return output

    def generate_no_match_vars(self):
        output = io.StringIO()
        for nmv in self.no_match_vars:
            print(f"var {nmv};", file=output)
        return output

    def generate_edit_row(self):
        output = io.StringIO()
        print(  # following is boiler-plate, but very imp code, Haribol
            f"""const datum = props.{self.model_props}.data.find(v => v.id === id);
    editId = id;""",
            file=output,
        )
        for field in self.fields.values():
            if field.type == "file":
                continue  # cannot edit file contents on server, Haribol
            source = self.grid_sources.get(field.name, field.name)
            print(f"editForm.{field.name} =", end=" ", file=output)
            print(f"datum.{source};", file=output)
            if field.type == "select":
                print(
                    f"{utils.no_match_var(field.match_value)} = datum.{field.match_value};",
                    file=output,
                )
        return output

    def generate_vue_props(self):
        output = io.StringIO()
        output.write("\n")
        if self.foreign_key:
            print(
                f"""{self.foreign_key.name}: Number,
    {self.foreign_key.prop}: Object,""",
                file=output,
            )
        for lookup in self.lookup_props:
            print(f"{lookup}: Array,", file=output)
        if output.getvalue() == "\n":
            output.truncate()
        return output

    def generate_controller_props(self):
        output = io.StringIO()
        if self.foreign_key:
            print(
                f"""'{self.foreign_key.name}' => ${self.foreign_key.prop}->{self.foreign_key.base_name},
    '{self.foreign_key.prop}' => {self.model.name}Helper::{self.foreign_key.prop}Details(),""",
                file=output,
            )
        for lookup in self.lookup_props:
            print(f"'{lookup}' => HelperClass::list()->get(),", file=output)
        return output

    def generate_controller_validation(self):
        output = io.StringIO()
        for field in self.fields.values():
            print(f"'{field.name}' => '',", file=output)
        return output

    def generate_store_data(self):
        output = io.StringIO()
        print(f"return {self.model.name}::create([", file=output)
        for field in self.fields.values():
            if field.type == "file":
                utils.note("File type inputs require to be saved to disk, Haribol!")
            print(f"'{field.base_name}' =>", end=" ", file=output)
            if field.type == "date":
                print(f"Utils::parseDate($validated['{field.name}']),", file=output)
            else:
                print(f"$validated['{field.name}'],", file=output)
        if self.foreign_key:
            print(
                f"'{self.foreign_key.base_name}' => request('{self.foreign_key.name}'),",
                file=output,
            )
        print("]);", file=output)
        return output

    def model_varname(self):
        return "$" + utils.first_char_lower(self.model.name)

    def generate_update_data(self):
        output = io.StringIO()
        varname = self.model_varname()
        for field in self.fields.values():
            if field.type == "file":
                utils.note("File type inputs require to be saved to disk, Haribol!")
            print(f"{varname}->{field.base_name} =", end=" ", file=output)
            if field.type == "date":
                print(f"Utils::parseDate($validated['{field.name}']);", file=output)
            else:
                print(f"$validated['{field.name}'];", file=output)
        print(f"LogActivityHelper::save({varname});", file=output)
        # print(f"return {varname};", file=output)
        return output

    funcs = [
        ("*** Avatar Heading ***", generate_avatar_heading),
        ("*** UI: addForm ***", generate_form_elements, "add"),
        ("*** UI: editForm ***", generate_form_elements, "edit"),
        ("*** Grid: parameters ***", generate_grid_parameters),
        ("*** Vue imports ***", generate_vue_imports),
        ("*** Vue props ***", generate_vue_props),
        ("*** Form: blanked ***", generate_blanked),
        ("*** Form: addForm ***", generate_form, "add"),
        ("*** Form: editForm ***", generate_form, "edit"),
        ("*** noMatchValue variables ***", generate_no_match_vars),
        ("*** editRow ***", generate_edit_row),
        ("*** Controller props ***", generate_controller_props),
        ("*** Controller: validation ***", generate_controller_validation),
        ("*** Store data ***", generate_store_data),
        ("*** Update data ***", generate_update_data),
    ]

    def generate(self):
        self.grid_columns = dict(sorted(self.grid_columns.items()))
        for func in self.funcs:
            print(func[0], file=self.output)
            try:
                self.output.write(func[1](self, *func[2:]).getvalue())
            except Exception as ex:
                utils.warn(ex)
            print("******\n", file=self.output)
        return self.output

    def hydrate(self):
        template = open("templates/Index.txt")
        output = open(f"output/Index.vue", "wt")
        repo = {
            "avatar_heading": self.generate_avatar_heading().getvalue(),
            "form_controls_for_adding": self.generate_form_elements("add").getvalue(),
            "form_controls_for_editing": self.generate_form_elements("edit").getvalue(),
            "grid_headings": f'"{self.grid_headings()}"',
            "model_props": self.model_props,
            "grid_column_types": f'"{self.grid_column_types()}"',
            "grid_fields": f'"{self.grid_fields()}"',
            "grid_sortable_fields": f'"{self.grid_sortable_fields()}"',
            "vue_imports": self.generate_vue_imports().getvalue(),
            "vue_props": self.generate_vue_props().getvalue(),
            "blanked": self.generate_blanked().getvalue(),
            "add_form": self.generate_form("add").getvalue(),
            "edit_form": self.generate_form("edit").getvalue(),
            "no_match_vars": self.generate_no_match_vars().getvalue(),
            "edit_row": self.generate_edit_row().getvalue(),
            "model_route": self.routes.url,
            "privy_suffix": f"_{self.routes.name}" if self.foreign_key else "",
        }
        while line := template.readline():
            hydrated = utils.hydrate(line, repo)
            print(hydrated, end="", file=output)
        template.close()
        output.close()

    def sortable(self, grid_column: str):
        return grid_column in map(
            lambda v: v.name, filter(lambda v: v.sortable(), self.grid_columns.values())
        )

    def field_specs(self, name: str):
        field = self.fields[name]
        return {
            'type': field.type,
            'title': field.title,
            'options': field.options,
            'focus': field.focus,
            'required': field.required,
        }
