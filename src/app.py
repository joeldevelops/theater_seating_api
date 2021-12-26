import quart.flask_patch
from quart import Quart, Response, jsonify
from flask_mongoengine import MongoEngine

from .errors import errors
from .seats import seats
from .venue import venue
from .wallet import wallet

app = Quart(__name__)
# app.register_blueprint(errors)
app.register_blueprint(seats)
app.register_blueprint(venue)
app.register_blueprint(wallet)

app.config.from_object("config")

db = MongoEngine()
db.init_app(app)

@app.route("/")
def index():
    stuff = {
      'groups': [1, 3, 4, 4, 5, 1, 2, 4],
      'rank': [[1, 2, 3, 4, 5, 6, 7, 8],
              [1, 2, 3, 4, 5, 6, 7, 8],
              [1, 2, 3, 4, 5, 6, 7, 8]]
    }
    return jsonify(stuff), 200
    # return Response("Index route not setup", 200)


@app.route("/health")
async def healthy():
    try:
        connection = db.connection.get_database("theater_seating_db")
        connection.command(
            "dbStats"
        )  # validate db is working
    except Exception as e:
        print(e)
        return Response("Unable to contact the DB", 500)

    return Response("ok", status=200)
