from flask_mongoengine import MongoEngine

db = MongoEngine()

# Venue is dynamic as we need to define an arbitrary number
# of sections with arbitrary names.
class Venue(db.DynamicDocument):
    name = db.StringField(required=True)


class Section(db.EmbeddedDocument):
    name = db.StringField(required=True)
    floor = db.StringField(required=True)
    total_seats = db.IntField(required=True)
    curved = db.BooleanField()
