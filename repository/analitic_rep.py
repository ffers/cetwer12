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
        items = []
        if period == "day":
            item = self.load_day()
            if item:
                items.append(item)
        if period == "all":
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
        start_time = current_time - timedelta(hours=14)
        start_time = start_time.replace(hour=14, minute=0, second=0,
                                        microsecond=0)
        stop_time = start_time + timedelta(days=1)
        item = Analitic.query.filter(
            Analitic.timestamp >= start_time,
            Analitic.timestamp <= stop_time,
            Analitic.period == "day"
            ).first()
        return item

    def load_period_sec(self, period, start, stop):
        item = Analitic.query.filter(
            Analitic.timestamp >= start,
            Analitic.timestamp <= stop,
            Analitic.period == period
            ).first()
        return item

    def add_first(self, args):
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
                orders=args[9]
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
            db.session.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    def update_work(self, id, args):
        try:
            product = Analitic.query.get_or_404(id)
            product.balance = args[0]
            product.wait = args[1]
            product.stock = args[2]
            product.inwork = args[3]
            product.income = args[4]
            db.session.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    def update_salary(self, id, args):
        try:
            product = Analitic.query.get_or_404(id)

            product.salary = args

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