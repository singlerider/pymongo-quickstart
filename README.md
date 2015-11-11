# pymongo-quickstart

This is a basic scaffold for your first Flask API interacting with MongoDB via
PyMongo.

## Installation

Setting up a virtual environment (ideally), installing dependencies, and gaining
credentials.

You'll need the MongoDB service running so the application can find the database.

Head to MongoDB's installation page to make sure you get it right:

https://docs.mongodb.org/manual/installation/

Finally, run the mongod service with:

`mongod`

### Virtual Environment

I would recommend running this in a virtual environment to keep your
dependencies in check. If you'd like to do that, run:

`sudo pip install virtualenv`

Followed by:

`virtualenv venv`

This will create an empty virtualenv in your project directory in a folder
called "venv." To enable it, run:

`source venv/bin/activate`

and your console window will be in that virtualenv state. To deactivate, run:

`deactivate`

### Dependencies

To install all dependencies locally (preferably inside your activated
virtualenv), run:

`pip install -r requirements.txt`

## To Run

Run

`./bot.py`

## To-do

Solve error message from DELETE request operation - it still goes through fine
