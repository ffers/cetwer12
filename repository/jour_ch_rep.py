from server_flask.db import db
from server_flask.models import JournalChange
from sqlalchemy import desc

class JourChRep:
    def load_all(self):
        items = JournalChange.query.order_by(desc(JournalChange.timestamp)).all()
        return items


    def load_article(self, article):
        item = JournalChange.query.filter_by(article=article).first()
        return item


    def add_(self, data):
        try:
            item = JournalChange(
                status=data[0],
                quantity=data[1],
                body=data[2],
                product_id=data[3],
                quantity_stock=data[4],
                event_date=data[5]
            )
            db.session.add(item)
            db.session.commit()
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