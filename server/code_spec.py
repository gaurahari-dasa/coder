import io
from InputSpecs import InputSpecs
from OutputSpecs import OutputSpecs


def save_model(model, output: io.StringIO):
    name = model["name"]
    cntxt_part = f", {model['cntxtName']}" if model["cntxtName"] else ""
    print(f"*** Model: {name}{cntxt_part} ***\n", file=output)


def save_routes(routes, output: io.StringIO):
    route = f"{routes['entityUrl']}({routes['entityRouteName']})"
    cntxt_part = (
        f", {routes['cntxtUrl']}({routes['cntxtRouteName']})"
        if routes["cntxtRouteName"]
        else ""
    )
    print(f"*** Routes: {route}{cntxt_part} ***\n", file=output)


def _save_field(field, output: io.StringIO):
    name = field["name"]
    alias_part = f" as {field['alias']}" if field["alias"] else ""
    name_part = name + alias_part
    foreign = f'$({field["foreign"]})' if field["foreign"] else None
    fillable = field["fillable"]
    input_specs = InputSpecs(**field["inputSpecs"]).__repr__() if fillable else None
    outputted = field["outputted"]
    output_specs = OutputSpecs(**field["outputSpecs"]).__repr__() if outputted else None
    morph_specs = f'~({field["morphSpecs"]})' if field["morphSpecs"] else None
    spec_str = ", ".join(
        filter(
            lambda x: x,
            [
                foreign,
                input_specs,
                output_specs,
                morph_specs,
            ],
        )
    )
    spec_part = f": {spec_str}" if spec_str else ""
    # if morph_specs or foreign or input_specs or output_specs:
    print(
        f"{name_part}{spec_part}",
        file=output,
    )


_primary_key = None


def _save_fields(fields, output: io.StringIO):
    # global _primary_key
    for field in filter(lambda f: not f["skipThis"], fields):
        _save_field(field, output)


def _save_tables(tables, output: io.StringIO):
    for table in filter(lambda t: not t["skipThis"], tables):
        print(f"\n** {table['name']} **", file=output)
        _save_fields(table["fields"], output)


def save_select_data(select_data, output: io.StringIO):
    global _primary_key
    _primary_key = select_data["entityTablePrimaryKey"]
    model_table = f"{select_data['entityTableName']}; {_primary_key}"
    cntxt_part = (
        f", {select_data['cntxtTableName']}; {select_data['cntxtTablePrimaryKey']}"
        if select_data["cntxtTablePrimaryKey"]
        else ""
    )
    print(f"*** SelectData: {model_table}{cntxt_part} ***", file=output)
    _save_tables(select_data["tables"], output)
