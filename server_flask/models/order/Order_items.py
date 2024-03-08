from server_flask.db import db


class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    orders_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id', name='fk_order_items_order_id', ondelete="CASCADE"), nullable=False)