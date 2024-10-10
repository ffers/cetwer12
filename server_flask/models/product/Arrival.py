from server_flask.db import db
from datetime import datetime


class Arrival(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    datetime_new = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)
    body_price = db.Column(db.Numeric(precision=8, scale=2))
    total_price = db.Column(db.Numeric(precision=8, scale=2))
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', name='fk_arrival_products_id'))
    products = db.relationship('Products', back_populates='arrival')

