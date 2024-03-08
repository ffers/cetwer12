from server_flask.db import db


class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50))
    orders = db.relationship("Orders", back_populates="payment_method")