import re
import io
from collections import namedtuple

import utils
from model import Model


class UserInput:

    ForeignKey = namedtuple("ForeignKey", ["name", "base_name"])

    class Field:
        focus_symbol = "@"
        required_symbol = "*"

        def __init__(self, name: str, base_name: str, specs: str, qualities: str):
            self.name = name
            self.base_name = base_name  # name in database, Haribol
            specs = [s.strip() for s in (specs.split(";") if specs else specs)]
            self.type = specs[0]
            self.title = utils.nullishIndex(specs, 1)
            self.options = utils.nullishIndex(specs, 2)
            self.focus = self.focus_symbol in qualities
            self.required = self.required_symbol in qualities

    def __init__(self, model: Model, model_table: str):
        self.fields = []
        self.lookups = set()
        self.foreign_key = None
        self.model = model
        self.model_table = model_table
        self.output = io.StringIO()

    def append_field(self, name, base_name, specs, qualities):
        self.fields.append(self.Field(name, base_name, specs, qualities))

    def assign_foreign_key(self, name, base_name):
        self.foreign_key = self.ForeignKey(name, base_name)

    def tackFocus(self, field):
        return " setFocus" if field.focus else ""

    def tackRequired(self, field):
        return " required" if field.required else ""

    def generate_typed_input(self, field, output, type="text"):
        print(
            f"""<FormInput type="{type}" class="mt-4" id="{field.name}" title="{field.title}"{self.tackFocus(field) + self.tackRequired(field)}
              v-model="{self.form_type}.{field.name}" :error="{self.form_type}.errors.{field.name}" />""",
            file=output,
        )

    def generate_text_input(self, field, output):
        self.generate_typed_input(field, output, type="text")

    def generate_email_input(self, field, output):
        self.generate_typed_input(field, output, type="email")

    def generate_date_input(self, field, output):
        self.generate_typed_input(field, output, type="date")

    def generate_select_input(self, field, output):
        self.lookups.add(field.options)
        print(
            f"""<FormSelect class="mt-4" id="{field.name}" title="{field.title}" :options="{field.options}"{self.tackFocus(field) + self.tackRequired(field)}
              v-model="{self.form_type}.{field.name}" :error="{self.form_type}.errors.{field.name}" />""",
            file=output,
        )

    def generate_checkbox_input(self, field, output):
        print(
            f"""<FormCheckBox class="mt-4" id="{field.name}" title="{field.title}" v-model="{self.form_type}.{field.name}" />""",
            file=output,
        )

    def generate_file_upload(self, field, output):
        print(
            f"""<FormFileUpload class="mt-4" id="{field.name}" title="{field.title}"{self.tackFocus(field) + self.tackRequired(field)}
              @pick="file => {self.form_type}.{field.name} = file" :error="{self.form_type}.errors.{field.name}" />""",
            file=output,
        )

    def generate_autocomplete(self, field, output):
        print(
            f"""<FormAutoComplete class="mt-4" id="{field.name}" title="{field.title}" :options="{field.options}"{self.tackFocus(field) + self.tackRequired(field)}
              v-model="{self.form_type}.{field.name}" :error="{self.form_type}.errors.{field.name}" />""",
            file=output,
        )

    def generate_control(self, field, output):
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
        self.form_type = form_type
        for field in self.fields:
            self.generate_control(field, output)
        return output

    def generate_pagination_urls(self):
        output = io.StringIO()
        iter_var = self.model.name.lower()
        print(
            rf"""
for (const {iter_var} of props.{self.model_table}.data) {{
    data.value.push({{ ...{iter_var} }});
}}

const prevUrl = props.{self.model_table}.prev_page_url;
const nextUrl = props.{self.model_table}.next_page_url;
""",
            file=output,
        )
        return output

    def generate_form(self, form_type: str):
        output = io.StringIO()
        if form_type == "editForm":
            print("id: null,", file=output)
        for field in self.fields:
            if form_type == "addForm" and field.type == "checkbox":
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
        if self.foreign_key:
            print(
                f"{self.foreign_key.name}: props.{self.foreign_key.name},",
                file=output,
            )
        return output

    def generate_edit_row(self):
        output = io.StringIO()
        print(  # following is boiler-plate, but very imp code, Haribol
            r"""
    editForm.id = id;
    const datum = data.value.find(v => v.id === id);
        """,
            file=output,
        )
        for field in self.fields:
            if field.type == "file":
                continue  # cannot edit file contents on server, Haribol
            print(f"editForm.{field.name} =", end=" ", file=output)
            if field.type == "checkbox":
                print(
                    f"!!datum.{field.name}; // cast to boolean, Haribol",
                    file=output,
                )
            else:
                print(f"datum.{field.name};", file=output)
        return output

    def generate_vue_props(self):
        output = io.StringIO()
        for lookup in self.lookups:
            print(f"{lookup}: Array,", file=output)
        return output

    def generate_controller_props(self):
        output = io.StringIO()
        for lookup in self.lookups:
            print(f"'{lookup}' => HelperClass::list()->get,", file=output)
        return output

    def generate_controller_validation(self):
        output = io.StringIO()
        for field in self.fields:
            print(f"'{field.name}' => '',", file=output)
        return output

    def generate_store_data(self):
        output = io.StringIO()
        print(f"return {self.model.name}::create([", file=output)
        for field in self.fields:
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
        print(f"{varname} = {self.model.name}::find(request('id'));", file=output)
        for field in self.fields:
            if field.type == "file":
                utils.note("File type inputs require to be saved to disk, Haribol!")
            print(f"{varname}->{field.base_name} =", end=" ", file=output)
            if field.type == "date":
                print(f"Utils::parseDate($validated['{field.name}']);", file=output)
            else:
                print(f"$validated['{field.name}'];", file=output)
        if self.foreign_key:
            print(
                f"{varname}->{self.foreign_key.base_name} = request('{self.foreign_key.name}');",
                file=output,
            )
        print(f"LogActivityHelper::save({varname});", file=output)
        print(f"return {varname};", file=output)
        return output

    funcs = [
        ("*** Pagination URLs ***", generate_pagination_urls),
        ("*** Form: addForm ***", generate_form, "addForm"),
        ("*** Form: editForm ***", generate_form, "editForm"),
        ("*** editRow ***", generate_edit_row),
        ("*** UI: addForm ***", generate_form_elements, "addForm"),
        ("*** UI: editForm ***", generate_form_elements, "editForm"),
        ("*** Vue props ***", generate_vue_props),
        ("*** Controller props ***", generate_controller_props),
        ("*** Controller: validation ***", generate_controller_validation),
        ("*** Store data ***", generate_store_data),
        ("*** Update data ***", generate_update_data),
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

    # def generate(self):
    #     self.generate_pagination_urls()
    #     self.generate_form("addForm")
    #     self.generate_form("editForm")
    #     self.generate_edit_row()
    #     self.generate_form_elements("addForm")
    #     self.generate_form_elements("editForm")
    #     self.generate_vue_props()
    #     self.generate_controller_props()
    #     self.generate_controller_validation()
    #     self.generate_store_server()
    #     self.generate_update_server()
    #     return self.output
