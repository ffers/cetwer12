from server_flask.db import db


class OrderedProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id', name='fk_ordered_product_order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id', name='fk_ordered_product_product_id'))
    products = db.relationship('Products', back_populates='ordered_product', overlaps="orders,products")