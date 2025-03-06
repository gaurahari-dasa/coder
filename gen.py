import re
import io

#pip install colorama
import colorama

colorama.init()

def printWarning(mesg, *args):
    print(f'{colorama.Fore.RED}{mesg}', args, colorama.Style.RESET_ALL)

def nullishIndex(ar:list, ix:int):
    try:
        return ar[ix]
    except IndexError:
        return None

class UiSection:

    class Field:
        def __init__(self, name:str, specs:str):
            self.name = name
            self.specs = [s.strip() for s in (specs.split(';') if specs else specs)]

    def __init__(self):
        self.lines = []
        self.fields = []
        self.output = io.StringIO()

    def append(self, line):
        self.lines.append(line)

    def appendField(self, name, specs):
        self.fields.append(self.Field(name, specs))

    def generate_text_input(self, field_name, title):
        print(f'''<FormInput class="mt-4" id="{field_name}" title="{title}"
            v-model="{self.form_type}.{field_name}" :error="{self.form_type}.errors.{field_name}" />''',
            file=self.output)

    def generate_email_input(self, field_name, title):
        print(f'''<FormInput type="email" class="mt-4" id="{field_name}" title="{title}"
            v-model="{self.form_type}.{field_name}" :error="{self.form_type}.errors.{field_name}" />''',
            file=self.output)

    def generate_select_input(self, field_name, title, options):
        print(f'''<FormSelect class="mt-4" id="{field_name}" title="{title}" :options="{options}"
            v-model="{self.form_type}.{field_name}" :error="{self.form_type}.errors.{field_name}" />''',
            file=self.output)
        
    def generate_checkbox_input(self, field_name, title):
        print(f'''<FormCheckBox class="mt-4" id="{field_name}" title="{title}" v-model="{self.form_type}.{field_name}" />''',
            file=self.output)

    def generate_control(self, field):
        ctrl_type = field.specs[0]
        title = nullishIndex(field.specs, 1)
        match ctrl_type:
            case 'text':
                self.generate_text_input(field.name, title)
            case 'select':
                self.generate_select_input(field.name, title, nullishIndex(field.specs, 2))
            case 'checkbox':
                self.generate_checkbox_input(field.name, title)
            case 'email':
                self.generate_email_input(field.name, title)
            case _:
                printWarning('Unknown control, Haribol!', field.name, ctrl_type)

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

    def append(self, line):
        self.lines.append(line)


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
        self.table, self.primary_key = [s.strip() for s in spec.split(',')]
        self.output = io.StringIO()
        self.tables = {}
        self.fields = None # track the current table, Haribol
        self.ui = UiSection()

    def segregateSpecs(self, field_name, specs):
        selectSpecs = None
        specs = [s.strip() for s in (specs.split(',') if specs else [])]
        for spec in specs:
            matched = re.match(r'[ ]*(~|t|i)[ ]*\((.*)\)', spec)
            if matched:
                match matched.group(1):
                    case 'i':
                        self.ui.appendField(field_name, matched.group(2))
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
            matched = re.match('([a-z_]+)(?:[ ]+as[ ]+([a-z_]+))?(?:[ ]*:(.*))?', line)
            if not matched:
                printWarning('DB field name spec is improper')
                exit()
            if self.fields is not None:
                self.fields.append(self.Field(
                    matched.group(1),
                    matched.group(2),
                    self.segregateSpecs(matched.group(1), matched.group(3))))

    def generateSelectData(self):
        print(f'*** SelectData: {self.table}, {self.primary_key} ***', file=self.output)
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
                print("'id'" if table == self.table and field.name == self.primary_key
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
        matched = re.match('\\*{3}[ ]*(.*?)(?::[ ]*(.*?))?[ ]*\\*{3}', line)
        if matched and matched.group(1) == 'UI':
            sections.append(UiSection())
            cur_sect = sections[-1]
        elif matched and matched.group(1) == 'SelectData':
            sections.append(SelectDataSection(matched.group(2)))
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
