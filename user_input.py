import re
import io

from utils import *

class UserInput:

    class Field:
        focus_symbol = '@'
        required_symbol = '*'

        def __init__(self, name:str, specs:str, qualities:str):
            self.name = name
            specs = [s.strip() for s in (specs.split(';') if specs else specs)]
            self.type = specs[0]
            self.title = nullishIndex(specs, 1)
            self.options = nullishIndex(specs, 2)
            self.focus = self.focus_symbol in qualities
            self.required = self.required_symbol in qualities

    def __init__(self):
        self.lines = []
        self.fields = []
        self.output = io.StringIO()

    def append(self, line):
        self.lines.append(line)

    def appendField(self, name, specs, qualities):
        self.fields.append(self.Field(name, specs, qualities))

    def tackFocus(self, field):
        return ' setFocus' if field.focus else ''

    def tackRequired(self, field):
        return ' required' if field.required else ''

    def generate_text_input(self, field):
        print(f'''<FormInput class="mt-4" id="{field.name}" title="{field.title}"{self.tackFocus(field) + self.tackRequired(field)}
              v-model="{self.form_type}.{field.name}" :error="{self.form_type}.errors.{field.name}" />''',
              file=self.output)

    def generate_email_input(self, field):
        print(f'''<FormInput type="email" class="mt-4" id="{field.name}" title="{field.title}"{self.tackFocus(field) + self.tackRequired(field)}
              v-model="{self.form_type}.{field.name}" :error="{self.form_type}.errors.{field.name}" />''',
              file=self.output)

    def generate_select_input(self, field):
        print(f'''<FormSelect class="mt-4" id="{field.name}" title="{field.title}" :options="{field.options}"{self.tackFocus(field) + self.tackRequired(field)}
              v-model="{self.form_type}.{field.name}" :error="{self.form_type}.errors.{field.name}" />''',
              file=self.output)
        
    def generate_checkbox_input(self, field):
        print(f'''<FormCheckBox class="mt-4" id="{field.name}" title="{field.title}" v-model="{self.form_type}.{field.name}" />''',
              file=self.output)
        
    def generate_file_upload(self, field):
        print(f'''<FormFileUpload class="mt-4" id="{field.name}" title="{field.title}"{self.tackFocus(field) + self.tackRequired(field)}
              @pick="file => {self.form_type}.{field.name} = file" :error="{self.form_type}.errors.{field.name}" />''',
              file=self.output)
        
    def generate_autocomplete(self, field):
        print(f'''<AutoComplete class="mt-4" id="{field.name}" title="{field.title}" :options="{field.options}"{self.tackFocus(field) + self.tackRequired(field)}
              v-model="{self.form_type}.{field.name}" :error="{self.form_type}.errors.{field.name}" />''',
              file=self.output)

    def generate_control(self, field):
        match field.type:
            case 'text':
                self.generate_text_input(field)
            case 'email':
                self.generate_email_input(field)
            case 'select':
                self.generate_select_input(field)
            case 'checkbox':
                self.generate_checkbox_input(field)
            case 'file':
                self.generate_file_upload(field)
            case 'auto':
                self.generate_autocomplete(field)
            case _:
                printWarning('Unknown control, Haribol!', field.name, field.type)

    def generate_form(self, form_type):
        print(f'*** UI: {form_type} ***', file=self.output)
        self.form_type = form_type
        for field in self.fields:
            self.generate_control(field)
        print('******\n', file=self.output)
        return self.output

    def generate(self):
        if not self.generate_form('addForm'):
            return None
            
        if not self.generate_form('editForm'):
            return None
        return self.output
