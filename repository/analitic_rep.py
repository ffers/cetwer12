from server_flask.models import Users, Orders, Products, OrderedProduct
from server_flask.models import ProductAnalitic, FinancAnalitic
from sqlalchemy import func
from server_flask.db import db


class AnaliticRep():
    def sum_product_quantity_order(self, product_id):
        sum_item = OrderedProduct.query((func.sum(OrderedProduct.quantity)).filter(OrderedProduct.product_id == product_id).scalar())
        return sum_item

    def sum_item(self):
        sum_item = db.session.query((func.sum(OrderedProduct.quantity)).scalar())
        return sum_item

    def body_product_price(self, product_id):
        body_price = db.session.query(Products.body_product_price).filter(Products.id == product_id).scalar()
        return body_price

    def quantity_product(self, product_id):
        quantity = db.session.query(Products.quantity).filter(Products.id == product_id).scalar()
        return quantity