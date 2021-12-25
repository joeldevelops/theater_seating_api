from flask_mongoengine import MongoEngine

db = MongoEngine()


class Entitlement(db.Document):
    user_id = db.StringField(required=True)
    venue_id = db.StringField(required=True)
    event_id = db.StringField(default="The Strokes Live")
    group_size = db.IntField(required=True)
    rank = db.StringField(required=True)
    preference = db.StringField(default="none")
