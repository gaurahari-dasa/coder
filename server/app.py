from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import main
import sections
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
