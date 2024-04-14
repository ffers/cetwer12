from server_flask.models import Users, Orders, Products, OrderedProduct
from server_flask.models import ProductAnalitic, FinancAnalitic
from sqlalchemy import func
from datetime import datetime, timedelta
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
        if not sum_product_sale:
            sum_product_sale = 0
        return sum_product_sale

    def get_money_sale_day(self):
        current_time = datetime.now()
        print(f"current_time {current_time}")
        start_time = current_time - timedelta(days=1)
        start_time = start_time.replace(hour=17, minute=0, second=0, microsecond=0)
        money_sale = (db.session.query(func.count(ProductAnalitic.money_in_sale))
                      .filter(ProductAnalitic.timestamp >= start_time,
                        ProductAnalitic.timestamp <= current_time).scalar())
        return money_sale

    def delete_item(self, id):
        task_to_delete = ProductAnalitic.query.get_or_404(id)
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return True

prod_an_rep = ProductAnaliticRep()




