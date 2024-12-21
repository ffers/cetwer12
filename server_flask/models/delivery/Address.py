from server_flask.db import db

class Address(db.Model): # має базою для данних по відділеням та адрес
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(50))
    city_name = db.Column(db.String(50))
    city_ref = db.Column(db.String(50))
    region = db.Column(db.String(50))
    area = db.Column(db.String(50))
    warehouse_option = db.Column(db.String(50))
    warehouse_text = db.Column(db.String(50))
    warehouse_ref = db.Column(db.String(50))
    description_delivery = db.Column(db.String(50))
    warehouse_text = db.Column(db.String(50))
    place_street = db.Column(db.String(50))
    place_number = db.Column(db.String(50))
    place_house = db.Column(db.String(50))
    place_flat = db.Column(db.String(50))
    street_ref = db.Column(db.String(50))
    title_city = db.Column(db.String(50))
    