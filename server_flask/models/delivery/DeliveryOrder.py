from server_flask.db import db

class DeliveryOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ref_ttn = db.Column(db.String(50), nullable=False)
    number_ttn = db.Column(db.String(50))
    ref_registr = db.Column(db.String(50))
    number_registr = db.Column(db.String(50))

    status_id = db.Column(db.Integer, db.ForeignKey(
        'delivery_status.id', name='fk_delivery_order_status_id'))
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id', name='fk_delivery_order_order_id'), nullable=False)

    delivery_status = db.relationship("DeliveryStatus", back_populates="delivery_order")
    orders = db.relationship("Orders", back_populates="delivery_order")
