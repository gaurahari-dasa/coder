import re
import io

class UiSection:
    def __init__(self):
        self.lines = []
        self.output = io.StringIO()

    def append(self, line):
        self.lines.append(line)

    def generate_text_input(self, field_name, title):
        print(f'''<FormInput class="mt-4" id="{field_name}" title="{title}"
            v-model="{self.form_type}.{field_name}" :error="{self.form_type}.errors.{field_name}" />''',
            file=self.output)

    def generate_select_input(self, field_name, title, options):
        print(f'''<FormSelect class="mt-4" id="{field_name}" title="{title}" :options="{options}"
            v-model="{self.form_type}.{field_name}" :error="{self.form_type}.errors.{field_name}" />''',
            file=self.output)
        
    def generate_checkbox_input(self, field_name, title):
        print(f'''<FormCheckBox class="mt-4" id="{field_name}" title="{title}" v-model="{self.form_type}.{field_name}" />''',
            file=self.output)

    def generate_control(self, field_name, ctrl_type, title, extra):
        if ctrl_type == 'text':
            self.generate_text_input(field_name, title)
        elif ctrl_type == 'select':
            self.generate_select_input(field_name, title, extra)
        elif ctrl_type == 'checkbox':
            self.generate_checkbox_input(field_name, title)
        else:
            print('Unknown control, Haribol!', field_name, ctrl_type)

    def generate_form(self, form_type):
        print(f'*** UI: {form_type} ***', file=self.output)
        self.form_type = form_type
        for line in self.lines:
            m = re.match('([^,]+)[ ]*:[ ]*([^,]+)[ ]*,[ ]*([^,]+)(?:[ ]*,[ ]*(.*))?', line)
            if m:
                if '_' in m.group(1):
                    ans = input('A field name has an underscore. Is this ok (enter \'y\' if it is)? ')
                    if ans.lower() != 'y':
                        return None
                self.generate_control(m.group(1), m.group(2), m.group(3), m.group(4))
        print('******\n', file=self.output)
        return self.output

    def generate(self):
        if not self.generate_form('addForm'):
            return None
            
        if not self.generate_form('editForm'):
            return None
        return self.output


class ModelSection:
    def __init__(self):
        self.lines = []

    def append(self, line):
        self.lines.append(line)


class SelectDataSection:
    # class Table:
    #     def __init__(self, name):
    #         self.name = name
    #         self.fields = []

    class Field:
        def __init__(self, name, alias):
            self.name = name
            self.alias = alias

    def __init__(self):
        # self.lines = []
        self.output = io.StringIO()
        self.tables = {}
        self.fields = None # track the current table, Haribol

    def append(self, line: str):
        if not (line := line.strip()):
            return
        matched = re.match('\\*{2}[ ]*(.*?)[ ]*\\*{2}', line)
        if matched:
            self.fields = self.tables.setdefault(matched.group(1), [])
        else:
            matched = re.match('([a-z_]+)(?:[ ]+as[ ]+([a-z_]+))?', line)
            if not matched:
                print('NOT Matched!')
                exit()
            if self.fields is not None:
                self.fields.append(self.Field(matched.group(1), matched.group(2)))

    def generate(self):
        print('*** SelectData ***', file=self.output)
        for table in self.tables:
            for field in self.tables[table]:
                alias = f' as {field.alias}' if field.alias else ''
                print(f'\'{table}.{field.name}{alias}\',', file=self.output)
        print('******\n', file=self.output)
        return self.output



sections = []
cur_sect = None

def read_sections():
    global cur_sect
    spec = open('input.spec')
    while (line := spec.readline()):
        matched = re.match('\\*{3}[ ]*(.*?)[ ]*\\*{3}', line)
        if matched and matched.group(1) == 'UI':
            sections.append(UiSection())
            cur_sect = sections[-1]
        elif matched and matched.group(1) == 'SelectData':
            sections.append(SelectDataSection())
            cur_sect = sections[-1]
        elif matched:
            print('section: <', matched.group(1), '>', sep='')
        elif cur_sect:
            cur_sect.append(line.strip())


read_sections()

output = open('output.txt', 'wt',)
for section in sections:
    if (gen := section.generate()):
        output.write(gen.getvalue())
