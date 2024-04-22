from server_flask.models import Analitic
from sqlalchemy import func
from server_flask.db import db
from datetime import datetime, timedelta


class AnaliticRep():

    def my_time(self):
        yield (datetime.utcnow())

    def load_all(self):
        items = Analitic.query.order_by(
            Analitic.timestamp
            ).all()
        return items

    def load_period(self, period):
        items = Analitic.query.filter_by(
            period=period
            ).all()
        return items

    def load_article(self, article):
        item = Analitic.query.filter_by(
            article=article).first()
        return item

    def load_day(self):
        current_time = next(self.my_time())
        print(current_time)
        start_time = current_time - timedelta(days=1)
        start_time = start_time.replace(
            hour=17, minute=0,
            second=0, microsecond=0
            )
        item = Analitic.query.filter(
            Analitic.timestamp >= start_time,
            Analitic.timestamp <= current_time,
            Analitic.period == "day"
            ).first()
        return item

    def add_(self, args):
        try:
            print(args)
            item = Analitic(
                torg=args[0],
                body=args[1],
                worker=args[2],
                prom=args[3],
                rozet=args[4],
                google_shop=args[5],
                insta=args[6],
                profit=args[7],
                period=args[8],
                orders=args[9],
                balance=args[10],
                wait=args[11],
                stock=args[12],
                inwork=args[13],
                salary=args[14],
                income=args[15]
            )
            db.session.add(item)
            db.session.commit()
            return True, None
        except Exception as e:
            return False, str(e)


    def update_(self, id, args):
        try:
            product = Analitic.query.get_or_404(id)
            product.torg = args[0]
            product.body = args[1]
            product.worker = args[2]
            product.prom = args[3]
            product.rozet = args[4]
            product.google_shop = args[5]
            product.insta = args[6]
            product.profit = args[7]
            product.period = args[8]
            product.orders = args[9]
            product.balance = args[10]
            product.wait = args[11]
            product.stock = args[12]
            product.inwork = args[13]
            product.salary = args[14]
            product.income = args[15]
            db.session.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    def update_quan(self, id, quantity):
        # try:
        product = Analitic.query.get_or_404(id)
        product.quantity = quantity
        db.session.commit()
        return True

    # except:
    #     return False

    def delete_(self, id):
        task_to_delete = Analitic.query.get_or_404(id)
        print(">>> Start delete in datebase")
        db.session.delete(task_to_delete)
        db.session.commit()
        print(">>> Delete in datebase")
        return True



an_rep = AnaliticRep()