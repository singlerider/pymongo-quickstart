#! /usr/bin/env python

from flask import Flask, request, jsonify, json
from pymongo import MongoClient
from bson import ObjectId
import requests

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)

client = MongoClient()
db = client.DATABASENAME
collection = db.COLLECTIONNAME

@app.errorhandler(404)
def page_not_found(e):
    return "CUSTOM ERROR"

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def device():
    if request.method == 'POST':
        param1 = request.args.get('param1')
        param2 = request.args.get('param2')
        document = collection.insert({"param1": param1, "param2": param2})
        return JSONEncoder().encode(document)
    if request.method == 'GET':
        _id = request.args.get('_id')
        result = collection.find_one({"_id": ObjectId(_id)})
        return JSONEncoder().encode(result)
    if request.method == 'PUT':
        _id = request.args.get('_id')
        param1 = request.args.get('param1')
        param2 = request.args.get('param2')
        result = collection.update({
                "_id": ObjectId(_id)
            },
            {
                "$set": {
                    "param1": param1,
                    "param2": param2
                },
            })
        if len(result) > 0:
            return JSONEncoder().encode(result)
        else:
            return {}
    if request.method == 'DELETE':
        _id = request.args.get('_id')
        result = collection.remove({"_id": ObjectId(_id)})

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0')
