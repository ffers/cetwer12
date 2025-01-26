from datetime import datetime
from server_flask.db import db
from DTO import ReceiptDTO


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    shift_id = db.Column(db.Integer, db.ForeignKey(
        'shift.id', name='fk_receipt_shift_id'))
    receipt_id = db.Column(db.String(255))

    def __init__(self, d: ReceiptDTO):
        """
        Кастомний конструктор для створення екземпляра UserToken з UserTokenDTO.
        """
        self.shift_id = d.shift_id
        self.receipt_id = d.receipt_id

    def update(self, d: ReceiptDTO):
        self.shift_id = d.shift_id or self.shift_id
        self.receipt_id = d.receipt_id or self.receipt_id
    
