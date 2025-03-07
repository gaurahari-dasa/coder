import re
import io

from utils import *
from user_input import UserInput

class SelectData:
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
        self.ui = UserInput()

    def assignSpecs(self, field_name:str, back_name:str, specs:str):
        selectSpecs = None
        specs = [s.strip() for s in (specs.split(',') if specs else [])]
        for spec in specs:
            matched = re.match(r'[ ]*(~|t|i)[ ]*\((.*)\)(.*)', spec)
            if matched:
                match matched.group(1):
                    case 'i':
                        self.ui.appendField(camel_case(field_name), back_name,
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
                self.assignSpecs(alias if alias else name, name, matched.group(3))))

    def generateSelectData(self):
        print(f'*** SelectData: {self.subject}, {self.primary_key} ***', file=self.output)
        for table in self.tables:
            for field in self.tables[table]:
                alias = f' as {field.alias}' if field.alias else ''
                print(f'\'{table}.{field.name}{alias}\',', file=self.output)
        # TODO: in subject table if primary key hasn't been selected include it, automatically, Haribol
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
        ui_code = self.ui.generate()
        if ui_code:
            self.output.write(ui_code.getvalue())
        return self.output
