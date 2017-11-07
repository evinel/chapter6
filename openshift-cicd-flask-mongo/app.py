import os

from flask import Flask, redirect, url_for, request, render_template, json, jsonify, Response
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(os.environ['MONGO_CONNECTION_URI'],27017)
db = client.tododb

@app.route('/')
def todo():

    _items = db.tododb.find()
    items = [item for item in _items]

    return render_template('todo.html', items=items)

@app.route('/gettasks')
def gettasks():

    _items = db.tododb.find()
    items = [item for item in _items]

    return Response(jsonify(items), mimetype='application/json'))
    
@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'name': request.form['name'],
        'description': request.form['completebydate']
    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('todo'))

@app.route('/addtask', methods=['POST'])
def addtask():

    json_data = request.get_json(force=True)
    db.tododb.insert_one(json_data)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
