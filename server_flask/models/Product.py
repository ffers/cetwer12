from server_flask.db import db
from datetime import datetime


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    article = db.Column(db.String(150), unique=True)
    product_name = db.Column(db.String(150))
    description = db.Column(db.String(300))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    body_product_price = db.Column(db.Float)
    orders = db.relationship('Orders', secondary='ordered_product', overlaps='ordered_product,orders,products')
    ordered_product = db.relationship('OrderedProduct', back_populates='products')
