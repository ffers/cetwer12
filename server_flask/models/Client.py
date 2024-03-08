from datetime import datetime
from server_flask.db import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    city = db.Column(db.String(150))
    warehouse = db.Column(db.Integer)
    phone = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(150), unique=True)