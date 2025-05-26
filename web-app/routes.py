import re
import io

import utils


class Routes:
    def __init__(self, specs: str):
        self.lines = []
        self.actions = []
        specs = [s.strip() for s in specs.split(",")]
        if not (m := re.match("(.*?)\((.*)\)", specs[0])):
            utils.error("Route definition is improper", specs[0])
        self.url = m.group(1)
        self.name = m.group(2)
        cntxt_specs:str = utils.nullishIndex(specs, 1)
        if cntxt_specs and not (m := re.match("(.*?)\((.*)\)", cntxt_specs)):
            utils.error("Context route definition is improper", cntxt_specs)
        self.cntxt_url = m.group(1) if cntxt_specs else None
        self.cntxt_name = m.group(2) if cntxt_specs else None

    def append(self, line):
        if not (line := line.strip()):
            return
        m = re.match("(.*?):(.*)")

    def generate(self):
        output = io.StringIO()
        print("*** Model: fillable ***", file=output)
        try:
            output.write(self.generate_fillable().getvalue())
        except Exception as ex:
            utils.warn(ex)
        print("******\n", file=output)
        return output

    def hydrate(self):
        # template = open("templates/routes.txt")
        # output = open(f"output/{self.name}.php", "wt")
        # repo = {
        # }
        # while line := template.readline():
        #     hydrated = utils.hydrate(line, repo)
        #     print(hydrated, end="", file=output)
        # template.close()
        # output.close()
        pass
