#! /usr/bin/env python

from flask import Flask, request, jsonify, json
from pymongo import MongoClient
from bson import ObjectId
import requests

app = Flask(__name__)

# Custom BSON (MongoDB JSON) to JSON encoder
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Database declarations - will instantiate automatically on first POST
client = MongoClient()
db = client.DATABASENAME
collection1 = db.COLLECTION1NAME
collection2 = db.COLLECTION2NAME

# Handle error404 however you want
@app.errorhandler(404)
def page_not_found(e):
    return "CUSTOM ERROR"

# Home page of our app, with GET, POST, PUT, DELETE methods allowed
@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def device():
    if request.method == "POST":
        # /?param1=result1&param2=result2
        # Method will create an {_id: ObjectId(HASH)} field in the document
        param1 = request.args.get("param1") # result1
        param2 = request.args.get("param2") # result2
        document = collection1.insert({"param1": param1, "param2": param2})
        return JSONEncoder().encode(document)
    if request.method == "GET":
        _id = request.args.get("_id") # Searches for {"_id": ObjectId(HASH)}
        result = collection1.find_one({"_id": ObjectId(_id)})
        return JSONEncoder().encode(result)
    if request.method == "PUT":
        _id = request.args.get("_id")
        param1 = request.args.get("param1")
        param2 = request.args.get("param2")
        # modifies an existing document with new paarameters
        result = collection1.update({
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
    if request.method == "DELETE":
        _id = request.args.get("_id")
        result = collection1.remove({"_id": ObjectId(_id)})

if __name__ == "__main__":
    app.run("0.0.0.0")
