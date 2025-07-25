



from server_flask.db import db
from datetime import datetime

class JournalBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    event_date = db.Column(db.DateTime)
    desription = db.Column(db.String(50))
    body = db.Column(db.Numeric(precision=8, scale=2))
    income = db.Column(db.Numeric(precision=8, scale=2))
    balance_id = db.Column(db.Integer, db.ForeignKey(
        'balance.id', name='fk_journal_balance_balance_id'))
    balance = db.relationship('Balance', backref='journal_balance')