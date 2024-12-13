from server_flask.db import db
from datetime import datetime

class DeliveryOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    city = db.Column(db.String(50), nullable=False)
    city_description = db.Column(db.String(50))
    region = db.Column(db.String(50))
    area = db.Column(db.String(50))
    city_ref = db.Column(db.String(50))
    warehouse = db.Column(db.String(50))