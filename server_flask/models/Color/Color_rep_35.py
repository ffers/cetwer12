from server_flask.db import db
from datetime import datetime

class Colorrep35(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Integer, unique=True)
    quantity = db.Column(db.Integer)