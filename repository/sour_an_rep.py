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
            item = ProductSource.query.filter_by(article=article).first()
            return item
        except Exception as e:
            return False, e


    # def add_(self, *data):
    #     try:
    #         item = ProductSource(
    #             status=data[0],
    #             quantity=data[1],
    #             body=data[2],
    #             product_id=data[3],
    #             quantity_stock=data[4]
    #         )
    #         db.session.add(item)
    #         db.session.commit()
    #         return True
    #     except Exception as e:
    #         return False, e


    # except:
    #     return False

    # def update_(self, id, data):
    #     try:
    #         product = ProductSource.query.get_or_404(id)
    #         product.article = data[0]
    #         product.name = data[1]
    #         product.price = data[2]
    #         product.quantity = data[3]
    #         product.money = data[4]
    #         db.session.commit()
    #         return True
    #     except:
    #         return False


    def update_quantity(self, id, quantity):
        try:
            product = ProductSource.query.get_or_404(id)
            product.quantity = quantity
            db.session.commit()
            return True
        except Exception as e:
            return False, e


    # except:
    #     return False

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

sour_an_rep = SourAnRep()