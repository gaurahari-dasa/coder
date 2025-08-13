from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import main
import json
import sections
import requests

# import schema_server
from validation_error import ValidationError

app = Flask(__name__)
CORS(app)
with open("sql.json") as f:
    config = json.load(f)


# schema_port = schema_server.run()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/read-spec")
def read_spec():
    main.read_sections()
    return {
        "model": sections.ix("Model").jsonify(),
        "routes": sections.ix("Routes").jsonify(),
        "selectData": sections.ix("SelectData").jsonify(),
    }


@app.route("/list-columns")
def list_columns():
    return main.list_columns(request.args["name"], request.args["cntxt_name"])


@app.post("/generate")
def generate():
    # main.save(request.json)
    main.generate()
    main.hydrate()
    return ""


@app.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    response = jsonify(
        {
            "message": error.message,
            "table_name": error.table_name,
            "back_name": error.back_name,
            "field_name": error.field_name,
        }
    )
    response.status_code = 422
    return response


@app.route("/reflect/table")
def reflect_table():
    # resp = requests.get(f"http://localhost:{schema_port}")
    table = requests.get(
        url=f"{config['reflectorUrl']}/api/v1/reflect/table/{request.args["name"]}",
        headers={"Accept": "application/json"},
    )
    return Response(
        response=table.content,
        status=table.status_code,
        content_type="application/json",
    )


@app.route("/reflect/fields")
def reflect_fields():
    # resp = requests.get(f"http://localhost:{schema_port}")
    params = {"table": request.args.get("table")}
    fields = requests.get(
        url=f"{config['reflectorUrl']}/api/v1/reflect/fields/{request.args["name"]}",
        headers={"Accept": "application/json"},
        params={key: value for key, value in params.items() if value is not None},
    )
    return Response(
        response=fields.content,
        status=fields.status_code,
        content_type="application/json",
    )
