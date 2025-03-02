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
                    ans = input('A field name has an underscore. Is this a mistake (enter \'y\' to bail out if it\'s a mistake)? ')
                    if ans.lower() == 'y':
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
    def __init__(self):
        self.lines = []

    def append(self, line):
        self.lines.append(line)

    def generate(self):
        pass


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
