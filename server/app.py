from flask import Flask
from flask_cors import CORS
from flask import request
import main
import sections

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

@app.post('/generate')
def generate():
    #main.save(request.json)
    main.generate()
    main.hydrate()
    return ''