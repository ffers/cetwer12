from server_flask.db import db
from datetime import datetime

class DayAnalitic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    torg = db.Column(db.Numeric(precision=8, scale=2))
    body = db.Column(db.Numeric(precision=8, scale=2))
    worker = db.Column(db.Numeric(precision=8, scale=2))
    prom = db.Column(db.Numeric(precision=8, scale=2))
    rozet = db.Column(db.Numeric(precision=8, scale=2))
    google_shop = db.Column(db.Numeric(precision=8, scale=2))
    insta = db.Column(db.Numeric(precision=8, scale=2))
    profit = db.Column(db.Numeric(precision=8, scale=2))