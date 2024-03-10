from server_flask.db import db
from datetime import datetime

class ProductAnalitic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    quantity_sale = db.Column(db.Integer)
    money_in_product = db.Column(db.Float)
    quantity_stok = db.Column(db.Integer)
