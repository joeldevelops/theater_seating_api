from flask import Flask, Response, json, jsonify, request
from flask_mongoengine import MongoEngine

from .errors import errors
from .seats import seats
from .venue import venue
from .wallet import wallet

app = Flask(__name__)
app.register_blueprint(errors)
app.register_blueprint(seats)
app.register_blueprint(venue)
app.register_blueprint(wallet)

app.config.from_object("config")

db = MongoEngine()
db.init_app(app)

@app.route("/")
def index(): 
    return Response("Index route not setup", 200)


@app.route("/health")
def healthy():
    try:
        connection = db.connection.get_database("theater_seating_db")
        res = connection.command(
            "dbStats"
        )  # validate db is working
    except:
        return Response("Unable to contact the DB", 500)

    return Response("ok", status=200)
