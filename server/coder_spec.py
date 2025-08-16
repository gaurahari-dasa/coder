import io


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
    morph_specs = field["morphSpecs"] if field["morphSpecs"] else ""
    foreign = field["foreign"] if field["foreign"] else ""
    fillable = field["fillable"]
    input_specs = field["inputSpecs"] if fillable else None
    searchable = field["searchable"]
    sortable = field["sortable"]
    sort_ordinal = field["sortOrdinal"]
    outputted = field["outputted"]
    output_specs = (
        "; ".join(s for s in field["outputSpecs"].values()) if outputted else None
    )
    if morph_specs or foreign or input_specs or output_specs:
        print(f"{name_part}: #1({output_specs})")  # TODO: get the order


_primary_key = None


def _save_fields(fields, output: io.StringIO):
    # global _primary_key
    for field in fields:
        _save_field(field, output)


def _save_tables(tables, output: io.StringIO):
    for table in tables:
        print(f"** {table['name']} **\n", file=output)
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
    print(f"*** SelectData: {model_table}{cntxt_part} ***\n", file=output)
    _save_tables(select_data["tables"], output)
