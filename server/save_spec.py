import io

def save_model(model):
    output = io.StringIO()
    name = model["name"]
    cntxt_part = f", {model['cntxtName']}" if model["cntxtName"] else ""
    print(f"*** Model: {name}{cntxt_part} ***\n", file=output)
    return output


def save_routes(routes):
    output = io.StringIO()
    route = f"{routes['entityUrl']}({routes['entityRouteName']})"
    cntxt_part = (
        f", {routes['cntxtUrl']}({routes['cntxtRouteName']})"
        if routes["cntxtRouteName"]
        else ""
    )
    print(f"*** Routes: {route}{cntxt_part} ***\n", file=output)
    return output


def save_fields(fields, output: io.StringIO):
    for field in fields:
        pass


def save_tables(tables, output: io.StringIO):
    for table in tables:
        print(f"** {table['name']} **")
        save_fields(table['fields'], output)


def save_select_data(select_data):
    output = io.StringIO()
    model_table = (
        f"{select_data['entityTableName']}; {select_data['entityTablePrimaryKey']}"
    )
    cntxt_part = (
        f", {select_data['cntxtTableName']}; {select_data['cntxtTablePrimaryKey']}"
        if select_data["cntxtTablePrimaryKey"]
        else ""
    )
    print(f"*** SelectData: {model_table}{cntxt_part} ***\n", file=output)
    save_tables(select_data["tables"], output)
    return output
