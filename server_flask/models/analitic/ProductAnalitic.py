from server_flask.db import db
from datetime import datetime

class ProductAnalitic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    quantity_sale = db.Column(db.Integer)
    money_in_product = db.Column(db.Numeric(precision=8, scale=2))
    quantity_stok = db.Column(db.Integer)
    money_in_sale = db.Column(db.Numeric(precision=8, scale=2))
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', name='fk_product_analitic_products_id'), unique=True)
    products = db.relationship('Products', back_populates='product_analitic')
