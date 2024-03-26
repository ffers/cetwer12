from server_flask.models import Users, Orders, Products, OrderedProduct
from server_flask.models import ProductAnalitic, FinancAnalitic
from sqlalchemy import func
from server_flask.db import db


class DayAnaliticRep():
    def body_product_price(self, product_id):
        body_price = db.session.query(Products.body_product_price).filter(Products.id == product_id).scalar()
        return body_price