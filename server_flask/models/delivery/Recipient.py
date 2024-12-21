from server_flask.db import db

class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_title = db.Column(db.String(50))
    recipient_first_name = db.Column(db.String(50))
    recipient_last_name = db.Column(db.String(50))
    recipient_second_name = db.Column(db.String(50))
    recipient_phone = db.Column(db.String(50))

    