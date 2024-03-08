from server_flask.db import db


class Colorrep45(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Integer, unique=True)
    quantity = db.Column(db.Integer)