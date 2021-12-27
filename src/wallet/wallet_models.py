from flask_mongoengine import MongoEngine

db = MongoEngine()


class Entitlement(db.DynamicDocument):
    user_id = db.IntField(required=True) # User ID is just group number here
    venue_id = db.ObjectIdField(required=True)
    event_id = db.StringField(default="The Strokes Live")
    rank = db.StringField(required=True)
    preference = db.StringField(default=None)
