from flask import Flask
from flask_cors import CORS
import main
import sections

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.post(
    "/read-spec",
)
def read_spec():
    main.read_sections()
    return {
        "model": sections.ix("Model").jsonify(),
        "routes": sections.ix("Routes").jsonify(),
    }
