from server_flask.db import db
from server_flask.models import JournalChange


class JourChRep:
    def load_all(self):
        products = JournalChange.query.order_by(JournalChange.timestamp).all()
        return products


    def load_article(self, article):
        item = JournalChange.query.filter_by(article=article).first()
        return item


    def add_(self, data):
        try:
            item = JournalChange(
                body=data[0]
            )
            db.session.add(item)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            return False, e


    # except:
    #     return False

    def update_(self, id, data):
        try:
            product = JournalChange.query.get_or_404(id)
            product.article = data[0]
            product.name = data[1]
            product.price = data[2]
            product.quantity = data[3]
            product.money = data[4]
            db.session.commit()
            return True
        except:
            return False


    def update_quan(self, id, quantity):
        # try:
        product = JournalChange.query.get_or_404(id)
        product.quantity = quantity
        db.session.commit()
        return True


    # except:
    #     return False

    def delete_(self, id):
        task_to_delete = JournalChange.query.get_or_404(id)
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return True

jour_ch_rep = JourChRep()