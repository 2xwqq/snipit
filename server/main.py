import random
import json
import os
import flask
import time
import datetime
from flask import abort
from flask import render_template
from flask import jsonify
from flask import request
from flask import Flask

app = Flask(__name__)

# DB = 'server/db.txt'
DB = 'server/snipit.sqlite'
con = sqlite3.connect(DB)

# Web application
@app.route('/')
def index():
    images = []
    cur = con.cursor()
    # TODO: Replace with query: 
    # rows = cur.execute('select * from shots')
    with open(DB) as f:
        for line in f:
          parts = line.rstrip().split(',')
          ts = parts[2]
          d = datetime.date.fromtimestamp(int(parts[2]))
          d = d.strftime('%d %B %Y')
          images.append({'id': parts[0], 'filename': parts[1], 'timestamp': parts[2], 'date': d})  
    return render_template('index.html', images=images)


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
    # TODO: Replace with query:
    # rows = cur.execute('select filename from shots where id=:id', {"id": id})
    # rows.fetchone()
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
    file.save(f'{os.getcwd()}/server/uploaded/{filename}')
    d = {'file': filename}
    number = random.randrange(99)
    ts = int(time.time())
    # TODO: Replace with query
    # cur.execute('insert into shots (id, filename, timestamp) values (56, "habr.png", 1623039296)')
    # con.commit()
    line = f'{number},{filename},{ts}\n'
    with open(DB, 'a') as f:
        f.write(line)
    return jsonify(d)


if __name__ == '__main__':
    app.run(debug=True)
