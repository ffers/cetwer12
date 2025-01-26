from datetime import datetime
from server_flask.db import db
from DTO import ReceiptDTO


class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    shift_id = db.Column(db.String(255))
    open = db.Column(db.DateTime)
    closed = db.Column(db.DateTime)
    receipts =  db.relationship('Receipt', backref='shift')

    def __init__(self, d: ReceiptDTO):
        self.shifd_id = d.shift_id
        self.open = d.open
        self.closed = d.closed

    def update(self):
        self.shifd_id = d.shift_id or self.shifd_id
        self.open = d.open or self.open
        self.closed = d.closed or self.closed 
