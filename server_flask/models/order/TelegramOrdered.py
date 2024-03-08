from server_flask.db import db


class TelegramOrdered(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(4096))
    confirmed_address_tg = db.relationship('ConfirmedAddressTg', backref='telegram_ordered', cascade='all, delete-orphan')
    np_address_tg = db.relationship('NpAddressTg', backref='telegram_ordered', cascade='all, delete-orphan')
    rozetka_address_tg = db.relationship('RozetkaAddressTg', backref='telegram_ordered', cascade='all, delete-orphan')
    ukr_address_tg = db.relationship('UkrAddressTg', backref='telegram_ordered', cascade='all, delete-orphan')
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id', name='fk_ordered_telegram_order_id'), nullable=False)
