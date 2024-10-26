from server_flask.db import db
from server_flask.models import ProductSource


class SourAnRep:
    def load_all(self):
        try:
            items = ProductSource.query.order_by(ProductSource.timestamp).all()
            return items
        except Exception as e:
            return False, e


    def load_article(self, article):
        try:
            print(article)
            item = ProductSource.query.filter_by(article=article).first()
            return item
        except Exception as e:
            db.session.rollback()
            print("Не найден артикль")
            return False, e

    def load_id(self, id):
        try:
            item = ProductSource.query.filter_by(id=id).first()
            return item
        except Exception as e:
            return False, e

    def update_source(self, id, data):
        try:
            product = ProductSource.query.get_or_404(id)
            product.article = data[0]
            product.name = data[1]
            product.price = data[2]
            product.quantity = data[3]
            product.money = data[4]
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False, e


    def update_quantity(self, id, quantity):
        try:
            product = ProductSource.query.get_or_404(id)
            product.quantity = quantity
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()q
            return False, e


    def delete_(self, id):
        try:
            task_to_delete = ProductSource.query.get_or_404(id)
            print(">>> Start delete in datebase")
            db.session.delete(task_to_delete)
            db.session.commit()
            print(">>> Delete in datebase")
            return True
        except Exception as e:
            return False, e

    def load_item(self, product_id):
        product = ProductSource.query.get_or_404(product_id)
        return product


    def add_product_source(self, data_list):
        try:
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
        except Exception as e:
            return False, e

    def delete_product_source(self, id):
        try:
            task_to_delete = ProductSource.query.get_or_404(id)
            print(">>> Start delete in datebase")
            db.session.delete(task_to_delete)
            db.session.commit()
            print(">>> Delete in datebase")
            return True
        except Exception as e:
            return False, e

sour_an_rep = SourAnRep()