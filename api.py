#! /usr/bin/env python

from datetime import datetime

from bson import ObjectId
from flask import Flask, json, request, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from wtforms import Form, TextField, SubmitField, validators

app = Flask(__name__)
Bootstrap(app)

# Custom BSON (MongoDB JSON) to JSON encoder


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# Database declarations - will instantiate automatically on first POST
client = MongoClient()
db = client.questiontwo
collection1 = db.proximity

# Handle error404 however you want


@app.errorhandler(404)
def page_not_found(e):
    return "CUSTOM ERROR"

# Home page of our app, with GET, POST, PUT, DELETE methods allowed


class DataForm(Form):
    me = TextField('Me', [validators.Required()])
    nearby = TextField('Nearby', [validators.Required()])
    submit = SubmitField("submit")


@app.route("/", methods=["GET", "POST", "DELETE"])
def device():
    proximity_date = datetime.now()
    if request.method == "GET":
        me = request.args.get("me")
        nearby = request.args.get("nearby")
        result = collection1.find(
            {"$query": {"me": me}, "$orderby": {"proximity_date": 1}}
        )
        alt_result = collection1.find(
            {"$query": {"me": nearby, "nearby": me}, "$orderby": {"proximity_date": 1}}
        )
        results = JSONEncoder().encode([x for x in result])
        alt_results = JSONEncoder().encode([x for x in alt_result])
        print results, alt_results
        # if type(result) == dict and type(alt_result) == dict:
        #     return JSONEncoder().encode(result)
        # elif type(result) == dict:
        return results
        # else:
        #     return render_template('404.html'), 404
    if request.method == "POST":
        me = request.args.get("me")  # result1
        nearby = request.args.get("nearby")
        document = collection1.insert(
            {"me": me, "nearby": nearby, "proximity_date": proximity_date}
        )
        return JSONEncoder().encode(document)
    if request.method == "DELETE":
        me = request.args.get("me")
        nearby = request.args.get("nearby")
        result = collection1.remove({"me": me, "nearby": nearby})
        return JSONEncoder().encode(result)


@app.route("/form", methods=["GET", "POST", "DELETE"])
def form_data():
    form = DataForm(request.form)
    if request.method == 'POST' and form.validate():
        me = request.form['me']
        nearby = request.form['nearby']
        return redirect("/?me={0}&nearby={1}".format(me, nearby), code=307)
    return render_template('form.html', form=form)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
