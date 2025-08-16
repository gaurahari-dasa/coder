from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from config import config, skip_reflect
import main
import sections
import requests

from validation_error import ValidationError

app = Flask(__name__)
CORS(app)


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


@app.post("/generate")
def generate():
    main.save(request.json)
    main.read_sections()
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
    resp = requests.get(
        url=f"{config['reflectorUrl']}/api/v1/reflect/table/{request.args["name"]}",
        headers={"Accept": "application/json"},
    )
    return Response(
        response=resp.content,
        status=resp.status_code,
        content_type="application/json",
    )


@app.route("/reflect/fields")
def reflect_fields():
    params = {"table": request.args.get("table")}
    resp = requests.get(
        url=f"{config['reflectorUrl']}/api/v1/reflect/fields/{request.args["name"]}",
        headers={"Accept": "application/json"},
        params={key: value for key, value in params.items() if value is not None},
    )
    if resp.ok:
        table = resp.json()
        table["fields"] = list(filter(
            lambda x: x.split(".")[1] not in skip_reflect, table["fields"]
        ))
        return table

    return Response(
        response=resp.content,
        status=resp.status_code,
        content_type="application/json",
    )
