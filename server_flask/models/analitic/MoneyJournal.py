from server_flask.db import db
from datetime import datetime, timezone

class MoneyJournal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    event_date = db.Column(db.DateTime)
    description = db.Column(db.String(50))
    movement = db.Column(db.Numeric(precision=8, scale=2))
    total = db.Column(db.Numeric(precision=8, scale=2))
