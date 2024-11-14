from server_flask.db import db
from datetime import datetime
 
class SourceDifference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    event_date = db.Column(db.DateTime)
    source_id = db.Column(db.Integer, db.ForeignKey(
        'product_source.id', name='fk_source_difference_product_source_id'))
    quantity_crm = db.Column(db.Integer)
    quantity_stock = db.Column(db.Integer)
    difference = db.Column(db.Integer)   
    sold = db.Column(db.Integer)
    comment = db.Column(db.String(300))
    product_source = db.relationship('ProductSource', back_populates='source_difference')  


 