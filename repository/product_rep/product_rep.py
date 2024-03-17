from server_flask.db import db
from server_flask.models import Products, ProductAnalitic


class ProductRep():
    def add_product(self, description, article, product_name, price, quantity):
        try:
            post = Products(description=description,
                            article=article,
                            product_name=product_name,
                            price=price,
                            quantity=quantity)
            db.session.add(post)
            db.session.commit()
            add_analitic = ProductAnalitic()
            return True
        except:
            return False

    def load_product_all(self):
        products = Products.query.order_by(Products.timestamp).all()
        return products

    def load_product_item(self, product_id):
        product = Products.query.get_or_404(product_id)
        return product

    def update_product_item(self, data, id):
        # try:
            product = Products.query.get_or_404(id)
            product.article = data[0]
            product.product_name = data[1]
            product.description = data[2]
            product.quantity = data[3]
            product.price = data[4]
            product.body_product_price = data[5]
            db.session.commit()
            return True
        # except:
        #     return False

