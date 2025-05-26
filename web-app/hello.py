from flask import Flask
import main
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.post('/read-spec',)
def read_spec():
    main.read_sections()
    return "Haribol, reading done!"