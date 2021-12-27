import quart.flask_patch
import os
import asyncio
from quart import Quart, Response, jsonify
from flask_mongoengine import MongoEngine
from flasgger import Swagger

from .errors import errors
from .seats import seats, create_seats
from .venue import venue, create_venue
from .wallet import wallet

app = Quart(__name__)
app.register_blueprint(errors)
app.register_blueprint(seats)
app.register_blueprint(venue)
app.register_blueprint(wallet)

app.config.from_object("config")

swagger = Swagger(app, template_file="../docs/swagger.yaml")

db = MongoEngine()
db.init_app(app)

@app.route("/")
def index():
    return Response("Index route not setup", 200)


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


@app.cli.command()
def initdb():
    name = "Carnegie Hall"
    section = [{
      "name": "Main Hall",
      "floor": "0",
      "total_seats": 24,
      "curved": False
    }]

    venue = asyncio.get_event_loop().run_until_complete(create_venue(name, section))

    new_seats = {
      "rank": "1",
      "seats": []
    }
    seat_number = 0
    for r in range(3):
        for c in range(8):
            seat_number += 1
            new_seats["seats"].append({
              "venue_id": venue.pk,
              "section": venue["Main Hall"]["name"],
              "seat_number": seat_number,
              "row": r + 1,
              "modifiers": ["aisle"] if (c == 0 or c == 7) else []
            })

    asyncio.get_event_loop().run_until_complete(create_seats(new_seats))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("PORT"), debug=True)