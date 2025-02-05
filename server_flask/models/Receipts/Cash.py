from datetime import datetime
from server_flask.db import db
from DTO import ReceiptDTO
 

class Cash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    cash_id = db.Column(db.String(255))
    fiscal_number = db.Column(db.String(255))
    name = db.Column(db.String(255))
    shifts =  db.relationship('Shift', backref='cash')

    def __init__(self, d: ReceiptDTO):
        self.cash_id = d.cash_id
        self.fiscal_number = d.fiscal_number
        self.name = d.name

    def update(self, d: ReceiptDTO):
        self.cash_id = d.cash_id or self.cash_id
        self.fiscal_number = d.fiscal_number or self.fiscal_number
        self.name = d.name or self.name
