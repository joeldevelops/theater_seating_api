from flask_mongoengine import MongoEngine

db = MongoEngine()


class Seat(db.Document):
    venue_id = db.StringField(required=True)
    section = db.StringField(required=True)
    seat_number = db.StringField(required=True)
    rank = db.StringField(required=True)
    row = db.StringField(required=True)
    aisle_seat = db.BooleanField(default=False)
    front_row = db.BooleanField(default=False)
