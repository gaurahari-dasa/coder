import re;

class UiSection:
    lines = []

    def __init__(self):
        pass

    def append(self, line):
        self.lines.append(line)


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
        elif matched:
            print('section: <', matched.group(1), '>', sep='')
        elif cur_sect:
            cur_sect.append(line.strip())

read_sections()

form_type = None
output = open('output.txt', 'wt',)

def generate_text_input(field_name, title):
    print(f'''
        <FormInput class="mt-4" id="{field_name}" title="{title}"
        v-model="{form_type}.{field_name}" :error="{form_type}.errors.{field_name}" />
          ''', file=output)

def generate_select_input(field_name, title, options):
    print(f'''
        <FormSelect class="mt-4" id="{field_name}" title="{title}" :options="{options}"
            v-model="{form_type}.{field_name}" :error="{form_type}.errors.{field_name}" />
          ''', file=output)
    
def generate_checkbox_input(field_name, title):
    print(f'''
        <FormCheckBox class="mt-4" id="{field_name}" title="{title}" v-model="{form_type}.{field_name}" />
          ''', file=output)

def generate_ui_control(field_name, ctrl_type, title, extra):
    if ctrl_type == 'text':
        generate_text_input(field_name, title)
    elif ctrl_type == 'select':
        generate_select_input(field_name, title, extra)
    elif ctrl_type == 'checkbox':
        generate_checkbox_input(field_name, title)
    else:
        print('Unknown control, Haribol!', field_name, ctrl_type)

def generate_add_ui():
    print('Generating UI for addForm ..')
    global form_type
    form_type = 'addForm'
    for line in sections[0].lines:
        m = re.match('([^,]+)[ ]*:[ ]*([^,]+)[ ]*,[ ]*([^,]+)(?:[ ]*,[ ]*(.*))?', line)
        if (m):
            generate_ui_control(m.group(1), m.group(2), m.group(3), m.group(4))

def generate_edit_ui():
    print('Generating UI for editForm ..')
    global form_type
    form_type = 'editForm'
    for line in sections[0].lines:
        m = re.match('([^,]+)[ ]*:[ ]*([^,]+)[ ]*,[ ]*([^,]+)(?:[ ]*,[ ]*(.*))?', line)
        if (m):
            generate_ui_control(m.group(1), m.group(2), m.group(3), m.group(4))

generate_add_ui()
generate_edit_ui()