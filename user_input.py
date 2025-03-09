import re
import io
from collections import namedtuple

from utils import *
from model import Model

class UserInput:

    ForeignKey = namedtuple('ForeignKey', ['name', 'base_name'])

    class Field:
        focus_symbol = '@'
        required_symbol = '*'

        def __init__(self, name:str, base_name:str, specs:str, qualities:str):
            self.name = name
            self.base_name = base_name # name in database, Haribol
            specs = [s.strip() for s in (specs.split(';') if specs else specs)]
            self.type = specs[0]
            self.title = nullishIndex(specs, 1)
            self.options = nullishIndex(specs, 2)
            self.focus = self.focus_symbol in qualities
            self.required = self.required_symbol in qualities

    def __init__(self, model:Model):
        self.fields = []
        self.foreign_key = None
        self.model = model
        self.output = io.StringIO()

    def appendField(self, name, base_name, specs, qualities):
        self.fields.append(self.Field(name, base_name, specs, qualities))

    def assign_foreign_key(self, name, base_name):
        self.foreign_key = self.ForeignKey(name, base_name)

    def tackFocus(self, field):
        return ' setFocus' if field.focus else ''

    def tackRequired(self, field):
        return ' required' if field.required else ''
    
    def generate_typed_input(self, field, type='text'):
        print(f'''<FormInput type="{type}" class="mt-4" id="{field.name}" title="{field.title}"{self.tackFocus(field) + self.tackRequired(field)}
              v-model="{self.form_type}.{field.name}" :error="{self.form_type}.errors.{field.name}" />''',
              file=self.output)

    def generate_text_input(self, field):
        self.generate_typed_input(field, type='text')

    def generate_email_input(self, field):
        self.generate_typed_input(field, type="email")
        
    def generate_date_input(self, field):
        self.generate_typed_input(field, type="date")

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
        print(f'''<FormAutoComplete class="mt-4" id="{field.name}" title="{field.title}" :options="{field.options}"{self.tackFocus(field) + self.tackRequired(field)}
              v-model="{self.form_type}.{field.name}" :error="{self.form_type}.errors.{field.name}" />''',
              file=self.output)

    def generate_control(self, field):
        match field.type:
            case 'text':
                self.generate_text_input(field)
            case 'email':
                self.generate_email_input(field)
            case 'date':
                self.generate_date_input(field)
            case 'select':
                self.generate_select_input(field)
            case 'checkbox':
                self.generate_checkbox_input(field)
            case 'file':
                self.generate_file_upload(field)
            case 'auto':
                self.generate_autocomplete(field)
            case _:
                warn('Unknown control, Haribol!', field.name, field.type)

    def generate_form(self, form_type):
        print(f'*** UI: {form_type} ***', file=self.output)
        self.form_type = form_type
        for field in self.fields:
            self.generate_control(field)
        print('******\n', file=self.output)
        return self.output
    
    def generate_store(self):
        print(f'*** Store data ***', file=self.output)
        print(f'return {self.model.name}::create([', file=self.output)
        for field in self.fields:
            if field.type == 'file':
                note('File type inputs require to be saved to disk, Haribol!')
            print(f"'{field.base_name}' =>", end=' ', file=self.output)
            if field.type == 'date':
                print(f"Utils::parseDate($validated['{field.name}']),", file=self.output)
            else:
                print(f"$validated['{field.name}'],", file=self.output)
        if self.foreign_key:
            print(f"'{self.foreign_key.base_name}' => request('{self.foreign_key.name}'),",
                   file=self.output)
        print(']);', file=self.output)
        print('******\n', file=self.output)
        return self.output
    
    def generate_update(self):
        print(f'*** Update data ***', file=self.output)
        varname = '$' + self.model.name.lower()
        print(f"{varname} = {self.model.name}::find(request('id'));", file=self.output)
        for field in self.fields:
            if field.type == 'file':
                note('File type inputs require to be saved to disk, Haribol!')
            print(f'{varname}->{field.base_name} =', end=' ', file=self.output)
            if field.type == 'date':
                print(f"Utils::parseDate($validated['{field.name}']);", file=self.output)
            else:
                print(f"$validated['{field.name}'];", file=self.output)
        if self.foreign_key:
            print(f"{varname}->{self.foreign_key.base_name} = request('{self.foreign_key.name}');",
                   file=self.output)
        print(f'LogActivityHelper::save({varname});', file=self.output)
        print(f'return {varname};')
        print('******\n', file=self.output)
        return self.output

    def generate(self):
        if not self.generate_form('addForm'):
            return None
            
        if not self.generate_form('editForm'):
            return None
        
        if not self.generate_store():
            return None
        
        if not self.generate_update():
            return None
        return self.output
