from server_flask.db import db
from datetime import datetime

class Analitic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    period = db.Column(db.String(50))
    torg = db.Column(db.Numeric(precision=8, scale=2))
    body = db.Column(db.Numeric(precision=8, scale=2))
    worker = db.Column(db.Numeric(precision=8, scale=2))
    prom = db.Column(db.Numeric(precision=8, scale=2))
    orders = db.Column(db.Integer)
    rozet = db.Column(db.Numeric(precision=8, scale=2))
    google_shop = db.Column(db.Numeric(precision=8, scale=2))
    insta = db.Column(db.Numeric(precision=8, scale=2))
    profit = db.Column(db.Numeric(precision=8, scale=2))
    balance = db.Column(db.Numeric(precision=8, scale=2))
    wait = db.Column(db.Numeric(precision=8, scale=2))
    stock = db.Column(db.Numeric(precision=8, scale=2))
    income = db.Column(db.Numeric(precision=8, scale=2))
    inwork = db.Column(db.Numeric(precision=8, scale=2))
    salary = db.Column(db.Numeric(precision=8, scale=2))
