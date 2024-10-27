from server_flask.db import db
from datetime import datetime

class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    balance = db.Column(db.Numeric(precision=10, scale=2))
    income = db.Column(db.Numeric(precision=10, scale=2))
    balance_fact = db.Column(db.Numeric(precision=10, scale=2))
    income_fact = db.Column(db.Numeric(precision=10, scale=2))

