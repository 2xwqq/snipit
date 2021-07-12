import json
import os
import flask
from flask import render_template
from flask import jsonify
from flask import request
from flask import Flask

app = Flask(__name__)

# Web application
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/images/<path:name>')
def images(name):
    return flask.send_from_directory('templates/images', name)


# API
# Test
@app.route('/v1/test', methods=['POST'])
def test():
    d = {'hello': request.json['key']}
    return jsonify(d)


@app.route('/v1/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    file.save(f'{os.getcwd()}/uploaded/{filename}')
    d = {'file': filename}
    return jsonify(d)
