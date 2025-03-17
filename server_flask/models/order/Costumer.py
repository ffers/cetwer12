from server_flask.db import db

class Costumer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    second_name = db.Column(db.String(50))
    full_name = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(50))
    orders = db.relationship("Orders", back_populates="costumer")