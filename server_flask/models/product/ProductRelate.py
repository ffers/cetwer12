from server_flask.db import db
from datetime import datetime


class ProductRelate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    article = db.Column(db.String(50))
    name = db.Column(db.String(150))
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', name='fk_product_relate_products_id'), nullable=False)
    products = db.relationship('Products', back_populates='product_relate')
    product_source_id = db.Column(db.Integer, db.ForeignKey(
        'product_source.id', name='fk_product_relate_product_source_id'))
    product_source = db.relationship("ProductSource", back_populates="product_relate")
