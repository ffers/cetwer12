from server_flask.db import db


class DeliveryMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50))
    orders = db.relationship("Orders", back_populates="delivery_method")


#  id |         name         | description
# ----+----------------------+-------------
#   1 | Нова Пошта           |
#   3 | Укрпошта             |
#   5 | Самовивіз            |
#   4 | Meest                |
#   2 | Точка видачі Rozetka |