from server_flask.db import db
from datetime import datetime

class JournalChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    event_date = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    body = db.Column(db.Numeric(precision=8, scale=2))
    income = db.Column(db.Numeric(precision=8, scale=2))
    quantity_stock = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product_source.id', name='fk_journal_change_product_source_id'))
    product = db.relationship('ProductSource', backref='journal_change')