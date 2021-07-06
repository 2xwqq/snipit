import json
from flask import render_template
from flask import jsonify
from flask import request
from flask import Flask

app = Flask(__name__)

# Web application
@app.route('/')
def index():
    return render_template('index.html')


# API
@app.route('/v1/upload', methods=['POST'])
def upload():
    d = {'hello': request.form['key']}
    return jsonify(d)