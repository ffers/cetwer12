from server_flask.models import Users, Orders, Products, OrderedProduct
from server_flask.models import ProductAnalitic, FinancAnalitic
from sqlalchemy import func


class AnaliticRep():
    def sum_order_product_quantity(self):
        resp = ProductAnalitic.query.order_by(Orders.timestamp.desc()).all()
        return resp

    def update_product_analitic(self):
        sum_item = ProductAnalitic.query((func.sum(OrderedProduct.quantity)).scalar())



