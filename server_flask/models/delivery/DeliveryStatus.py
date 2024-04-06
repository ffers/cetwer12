from server_flask.db import db


class DeliveryStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    name = db.Column(db.String(50))
    description = db.Column(db.String(300))
    delivery_order = db.relationship("DeliveryOrder", back_populates="delivery_status")