from flask import request
from flask import Flask, jsonify
from flask_cors import CORS
from ConexionBD import *
from pipe import *

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# *************************************************************************
# *************************************************************************
# *************************************************************************


if __name__ == "__main__":
    app.run(debug=True)