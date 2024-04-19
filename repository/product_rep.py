from server_flask.db import db
from server_flask.models import (Products,
                                 ProductAnalitic,
                                 ProductRelate,
                                 ProductSource)


class ProductRep():
    def add_product(self, description, article, product_name, price, quantity):
        try:
            product = Products(description=description,
                            article=article,
                            product_name=product_name,
                            price=price,
                            quantity=quantity)
            db.session.add(product)
            db.session.commit()
            add_analitic = ProductAnalitic(product_id=product.id)
            db.session.add(add_analitic)
            db.session.commit()
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
        try:
            product = Products.query.get_or_404(id)
            product.article = data[0]
            product.product_name = data[1]
            product.description = data[2]
            product.quantity = data[3]
            product.price = data[4]
            product.body_product_price = data[5]
            db.session.commit()
            return True
        except:
            return False

    def update_after_arrival(self, combined_list):
        for item in combined_list:
            datetime_new, product_id, quantity, price, total = item
            product = Products.query.get_or_404(product_id)
            product.quantity = quantity + product.quantity
            product.body_product_price = price
            db.session.commit()
        return True

    def delete_product(self, id):
        task_to_delete = Products.query.get_or_404(id)
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return True

    def changeBodyPrice(self):
        products = self.load_product_all()
        for item in products:
            if not item.body_product_price:
                item.body_product_price = 0

    # relate product

    def add_product_relate(self, data_list):
        try:
            item = ProductRelate(
                article=data_list[0],
                name=data_list[1],
                quantity=data_list[2],
                product_id=data_list[3]
            )
            db.session.add(item)
            db.session.commit()
            db.session.close()
            return True
        except:
            return False

    def update_product_relate(self, data, id):
        try:
            product = ProductRelate.query.get_or_404(id)
            product.article = data[0]
            product.name = data[1]
            product.quantity = data[2],
            product.product_id = data[3]
            db.session.commit()
            return True
        except:
            return False

    def load_product_relate(self):
        products = ProductRelate.query.order_by(ProductRelate.timestamp).all()
        return products

    def load_product_relate_item(self, product_id):
        item = ProductRelate.query.get_or_404(product_id)
        return item

    def load_prod_relate_product_id(self, id):
        item = ProductRelate.query.filter_by(product_id=id).first()
        return item

    def load_prod_relate_product_id_all(self, id):
        item = ProductRelate.query.filter_by(product_id=id).all()
        return item

    def load_product_source_item(self, product_id):
        product = ProductSource.query.get_or_404(product_id)
        return product

    def delete_product_relate(self, id):
        task_to_delete = ProductRelate.query.get_or_404(id)
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return True

    def load_product_source_all(self):
        products = ProductSource.query.order_by(ProductSource.timestamp).all()
        return products

    def load_product_source_article(self, article):
        item = ProductSource.query.filter_by(article=article).first()
        return item


    def add_product_source(self, data_list):
        # try:
            item = ProductSource(
                article=data_list[0],
                name=data_list[1],
                price=data_list[2],
                quantity=data_list[3],
                money=data_list[4]
            )
            db.session.add(item)
            db.session.commit()
            db.session.close()
            return True
        # except:
        #     return False

    def update_product_source(self, id, data):
        try:
            product = ProductSource.query.get_or_404(id)
            product.article = data[0]
            product.name = data[1]
            product.price = data[2]
            product.quantity = data[3]
            product.money = data[4]
            db.session.commit()
            return True
        except:
            return False

    def update_prod_sour_quan(self, id, quantity):
        # try:
            product = ProductSource.query.get_or_404(id)
            product.quantity = quantity
            db.session.commit()
            return True
        # except:
        #     return False

    def delete_product_source(self, id):
        task_to_delete = ProductSource.query.get_or_404(id)
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return True




prod_rep = ProductRep()



