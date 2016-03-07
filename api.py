#! /usr/bin/env python

from datetime import datetime

from bson import ObjectId
from flask import Flask, json, request, render_template, redirect
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from wtforms import Form, TextField, SubmitField, validators
import requests
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app)
Bootstrap(app)


class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = MongoClient()
db = client.questiontwo
collection1 = db.proximity


@app.errorhandler(404)
def page_not_found(e):
    return "CUSTOM ERROR"


class DataForm(Form):
    me = TextField('Me', [validators.Required()])
    nearby = TextField('Nearby', [validators.Required()])
    submit = SubmitField("submit")


class DisplayForm(Form):
    me = TextField('Me')
    nearby = TextField('Nearby')
    submit = SubmitField("submit")


class DeleteForm(Form):
    _id = TextField('_id', [validators.Required()])
    submit = SubmitField("submit")


@app.route("/", methods=["GET", "POST", "DELETE"])
def device():
    me = request.args.get("me")
    nearby = request.args.get("nearby")
    proximity_date = datetime.now()
    if request.method == "GET":
        result = collection1.find(
            {
                "$query": {"me": me}, "$orderby": {"proximity_date": 1}
            }
        )
        alt_result = collection1.find(
            {
                "$query": {"me": nearby, "nearby": me},
                "$orderby": {"proximity_date": 1}
            }
        )
        # iteration required to separate entries as usable data
        results = [x for x in result if x.get(
            "me") is not None and x.get("nearby") is not None]
        alt_results = [x for x in alt_result if x.get(
            "me") is not None and x.get("nearby") is not None]
        print results, alt_results
        if len(results) > 0 and len(alt_results) > 0:
            return JSONEncoder().encode(results)
        else:
            return render_template('404.html'), 404
    if request.method == "POST":
        result = collection1.find_one({"me": me, "nearby": nearby})
        if not result:
            document = collection1.insert(
                {"me": me, "nearby": nearby, "proximity_date": proximity_date}
            )
            return JSONEncoder().encode(document)
        else:
            _id = JSONEncoder().encode(result.get("_id"))
            updated = collection1.update(
                {"_id": ObjectId(_id.strip("\""))}, {
                    "$set": {"proximity_date": proximity_date}
                }
            )
            return JSONEncoder().encode(updated)
    if request.method == "DELETE":
        result = collection1.find_one({"me": me, "nearby": nearby})
        if result:
            collection1.remove({"me": me, "nearby": nearby})
            return JSONEncoder().encode(result)
        else:
            return render_template('404.html'), 404


@app.route("/input-form", methods=["GET", "POST"])
def input_form():
    form = DataForm(request.form)
    if request.method == 'POST' and form.validate():
        me = request.form['me']
        nearby = request.form['nearby']
        return redirect("/?me={0}&nearby={1}".format(me, nearby), code=307)
    return render_template('form.html', form=form)


@app.route("/delete-form", methods=["GET", "POST"])
def delete_form():
    form = DeleteForm(request.form)
    if request.method == 'POST' and form.validate():
        _id = request.form['_id']
        return redirect("/display?_id={0}".format(_id), code=307)
    return render_template('form.html', form=form)


@app.route("/display", methods=["GET", "POST"])
def display():
    form = DisplayForm(request.form)
    data = list(collection1.find())
    if request.method == 'POST' and form.validate():
        me = request.form.get('me')
        nearby = request.form.get('nearby')
        _id = request.form.get('_id')
        if me is not None and nearby is not None:
            return redirect("/?me={0}&nearby={1}".format(me, nearby), code=307)
        if _id is not None:
            result = collection1.find_one({"_id": ObjectId(_id.strip("\""))})
            collection1.remove({"_id": ObjectId(_id.strip("\""))})
            return JSONEncoder().encode(result)
        return render_template('404.html'), 404
    for entry in data:
        inverse_match = collection1.find_one(
            {"me": entry.get("nearby"), "nearby": entry.get("me")})
        if inverse_match is not None:
            entry["color"] = "green"
        else:
            entry["color"] = "red"
    return render_template('display.html', form=form, data=data)


if __name__ == "__main__":
    app.run("0.0.0.0", threaded=True, debug=True)
