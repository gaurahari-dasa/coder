import re
import io

#pip install colorama
import colorama

colorama.init()

def printWarning(mesg, *args):
    print(f'{colorama.Fore.RED}{mesg}', args, colorama.Style.RESET_ALL)

def printError(mesg, *args):
    print(f'{colorama.Fore.YELLOW}{mesg}', args, colorama.Style.RESET_ALL)

def nullishIndex(ar:list, ix:int):
    try:
        return ar[ix]
    except IndexError:
        return None

identifier = '[a-zA-Z0-9_]+'

class InputSection:

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


class ModelSection:
    def __init__(self):
        self.lines = []
        self.output = io.StringIO()

    def append(self, line):
        self.lines.append(line)

    def generate(self):
        print('*** Model: fillable ***', file=self.output)
        for line in self.lines:
            matched = re.match(f'[ ]*({identifier})', line)
            if matched:
                print(f"'{matched.group(1)}',", file=self.output)
        print('******', file=self.output)
        return self.output


def camel_case(name:str):
    return re.sub('_(.)', lambda v: v.group(1).upper(), name)


class SelectDataSection:
    # class Table:
    #     def __init__(self, name):
    #         self.name = name
    #         self.fields = []

    class Field:
        def __init__(self, name:str, alias:str, specs:str):
            self.name = name
            self.alias = alias
            self.specs = specs

    def __init__(self, spec:str):
        self.subject, self.primary_key = [s.strip() for s in spec.split(';')]
        self.output = io.StringIO()
        self.tables = {}
        self.fields = None # track the current table, Haribol
        self.ui = InputSection()

    def segregateSpecs(self, field_name, specs):
        selectSpecs = None
        specs = [s.strip() for s in (specs.split(',') if specs else [])]
        for spec in specs:
            matched = re.match(r'[ ]*(~|t|i)[ ]*\((.*)\)(.*)', spec)
            if matched:
                match matched.group(1):
                    case 'i':
                        self.ui.appendField(camel_case(field_name),
                                            matched.group(2), matched.group(3))
                    case '~':
                        selectSpecs = matched.group(2)
                    case _:
                        printWarning('Unheard specs type, Haribol')
        return selectSpecs

    def append(self, line: str):
        if not (line := line.strip()):
            return
        matched = re.match('\\*{2}[ ]*(.*?)[ ]*\\*{2}', line)
        if matched:
            self.fields = self.tables.setdefault(matched.group(1), [])
        else:
            matched = re.match(f'({identifier})(?:[ ]+as[ ]+({identifier}))?(?:[ ]*:(.*))?', line)
            if not matched:
                printError('DB field name spec is improper, Haribol!')
                exit()
            if self.fields is None:
                printError('No table name in specs, Haribol!')
                exit()
            name = matched.group(1)
            alias = matched.group(2)
            self.fields.append(self.Field(name, alias,
                self.segregateSpecs(alias if alias else name, matched.group(3))))

    def generateSelectData(self):
        print(f'*** SelectData: {self.subject}, {self.primary_key} ***', file=self.output)
        for table in self.tables:
            for field in self.tables[table]:
                alias = f' as {field.alias}' if field.alias else ''
                print(f'\'{table}.{field.name}{alias}\',', file=self.output)
        print('******\n', file=self.output)

    def generatePagination(self):
        print('*** Paginate (SelectData) ***', file=self.output)
        for table in self.tables:
            for field in self.tables[table]:
                alias = field.alias if field.alias else field.name
                print("'id'" if table == self.subject and field.name == self.primary_key
                       else f"'{camel_case(alias)}'", '=>', end=' ', file=self.output)
                match field.specs:
                    case None: print(f"$item->{alias},", file=self.output)
                    case 'file': print(f'Storage::url($item->{alias}),', file=self.output)
                    case 'date-only': print(f'Utils::formatDateJs($item->{alias}, DateFormatJs::OnlyDate),',
                                             file=self.output)
                    case 'date-time': print(f'Utils::formatDateJs($item->{alias}, DateFormatJs::DateTime),',
                                             file=self.output)
                    case _: printWarning('Unknow transformation type, Haribol')

        print('******\n', file=self.output)

    def generate(self):
        self.generateSelectData()
        self.generatePagination()
        output.write(self.ui.generate().getvalue())
        return self.output


sections = []
cur_sect = None

def read_sections():
    global cur_sect
    spec = open('input.spec')
    while (line := spec.readline()):
        line = line.strip()
        if not line or line.startswith('#'): # comment, Haribol
            continue
        matched = re.match('\\*{3}[ ]*(.*?)(?::[ ]*(.*?))?[ ]*\\*{3}', line)
        if matched:
            match (matched.group(1)):
                case 'SelectData':
                    sections.append(SelectDataSection(matched.group(2)))
                case 'Model':
                    sections.append(ModelSection())
                case _:
                    print('section: <', matched.group(1), '>', sep='')
                    continue
            cur_sect = sections[-1]
        elif cur_sect:
            cur_sect.append(line)


read_sections()

output = open('output.txt', 'wt',)
for section in sections:
    if (gen := section.generate()):
        output.write(gen.getvalue())
