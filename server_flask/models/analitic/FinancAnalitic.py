from server_flask.db import db
from datetime import datetime

class FinancAnalitic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    balance = db.Column(db.Float)
    order_quantity = db.Column(db.Float)
    rest_start_month = db.Column(db.Float)
    expect_start_month = db.Column(db.Float)
    expect_payment = db.Column(db.Float)
    body = db.Column(db.Float)
    product_balance = db.Column(db.Float)
    salary = db.Column(db.Float)
    debet = db.Column(db.Float)
    credit = db.Column(db.Float)
    working_money = db.Column(db.Float)