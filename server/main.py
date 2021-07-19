import random
import json
import os
import flask
import time
from flask import abort
from flask import render_template
from flask import jsonify
from flask import request
from flask import Flask

app = Flask(__name__)

DB = 'db.txt'

# Web application
@app.route('/')
def index():
    # TODO: Read db.txt file and populate file data:
    #   - random number
    #   - filename
    #   - timestamp
    # Tip: Use
    #   - open(),
    #   images = []
    # >>> with open('db.txt') as f:
    # ...   for line in f:
    #           print(line) 
    #           # Use line
    #   - .split(',')
    #   - images.append({'id': '...', 'filename': '...', 'timestamp': '...'})
    # Part 1: Populate "images"
    # Part 2: Use "images" in template
    images = [
        # Example:
        {
            'id': '23',
            'filename': 'epoch.png',
            'timestamp': '1624335296'
        },
        # ...
        # For every file line
    ]
    return render_template('index.html', image=images)


@app.route('/<path:id>')
def shot(id):
    name = image_by_id(id)
    if not name:
        abort(404)
    return flask.send_from_directory('uploaded', name)


@app.route('/images/<path:name>')
def images(name):
    return flask.send_from_directory('templates/images', name)


def image_by_id(id):
    """Find filename from id."""
    with open(DB) as f:
        for line in f:
            line = line.rstrip()
            row = line.split(',')
            if row[0] == id:
                return row[1]
    return None


# API
# Test
@app.route('/v1/test', methods=['POST'])
def test():
    number = random.randrange(99)
    with open('db.txt', 'a') as f:
        f.write(f'\n{number}')
    d = {'hello': number}
    return jsonify(d)


@app.route('/v1/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = file.filename
    file.save(f'{os.getcwd()}/uploaded/{filename}')
    d = {'file': filename}
    number = random.randrange(99)
    ts = int(time.time())
    line = f'{number},{filename},{ts}\n'
    with open('db.txt', 'a') as f:
        f.write(line)
    return jsonify(d)


if __name__ == '__main__':
    app.run(debug=True)
