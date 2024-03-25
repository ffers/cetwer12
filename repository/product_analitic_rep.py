from server_flask.models import Users, Orders, Products, OrderedProduct
from server_flask.models import ProductAnalitic, FinancAnalitic
from sqlalchemy import func
from server_flask.db import db


class ProductAnaliticRep():
    def body_product_price(self, product_id):
        body_price = db.session.query(Products.body_product_price).filter(Products.id == product_id).scalar()
        return body_price

    def quantity_product(self, product_id):
        quantity = db.session.query(Products.quantity).filter(Products.id == product_id).scalar()
        return quantity

    def update_product_analitic(self, *args):
        try:
            item = ProductAnalitic.query.filter_by(product_id=args[0]).first()
            item.money_in_product = args[1]
            item.quantity_sale = args[2]
            item.money_in_sale = args[3]
            db.session.commit()
            return True
        except:
            return False

    def item_product_analitic(self, product_id):
        item = ProductAnalitic.query.filter_by(product_id=product_id).first()
        return item

    def all_product_analitic(self):
        item_all = ProductAnalitic.query.order_by(ProductAnalitic.timestamp.desc()).all()
        return item_all

    def add_product_analitic(self, product_id):
        try:
            print("СРАБОТАЛ АПДЕЙТ АНАЛІТІК")
            prod_analitic = ProductAnalitic(product_id=product_id)
            db.session.add(prod_analitic)
            db.session.commit()
        except:
            return False

    def search_an_product_id(self, product_id):
        prod_an_item = ProductAnalitic.query.filter_by(product_id=product_id).first()
        return prod_an_item

    def get_sum_product_sale(self, product_id):
        sum_product_sale = db.session.query(func.sum(OrderedProduct.quantity)).filter(OrderedProduct.product_id == product_id).scalar()
        return sum_product_sale




