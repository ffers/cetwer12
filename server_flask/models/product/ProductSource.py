from server_flask.db import db
from datetime import datetime

class ProductSource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    article = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(150))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(precision=8, scale=2))
    money = db.Column(db.Numeric(precision=10, scale=2))
    product_relate = db.relationship("ProductRelate", back_populates="product_source")
    source_difference = db.relationship('SourceDifference', back_populates='product_source')





