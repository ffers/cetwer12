from server_flask.db import db

class ConfirmedAddressTg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer)
    chat_id = db.Column(db.Integer)
    tg_ord_id = db.Column(db.Integer, db.ForeignKey(
        'telegram_ordered.id', name='fk_telegram_ordered_conf_addr_tg_id'), nullable=False)