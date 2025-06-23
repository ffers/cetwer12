from server_flask.models import Analitic
from sqlalchemy import func
from server_flask.db import db
from datetime import datetime, timedelta
from utils import OC_logger, DEBUG

from domain.models.analitic_dto import AnaliticDto

class UpdateProblemRepo(Exception):
    pass

class LoadPeriodTime(Exception):
    pass

class AnaliticNotUnique(Exception):
    pass

class AnaliticRep():
    def __init__(self):
        self.logger = OC_logger.oc_log('analitic_rep')

    def my_time(self):
        yield (datetime.utcnow())

    def check_period(self, period, time):
        existing = Analitic.query.filter_by(
            period=period,
            timestamp=time
        ).first()

        if existing:
            raise AnaliticNotUnique(f"Вже є запис на цей період - {period}")

    def add_row(self, period, time):
        try:
            self.check_period(period, time)
            i = Analitic(
                timestamp=time,
                torg=0,
                body=0,
                worker=0,
                prom=0,
                rozet=0,
                google_shop=0,
                insta=0,
                profit=0,
                period=period,
                orders=0,
                salary=0,
                balance=0,
                wait=0,
                stock=0,
                inwork=0,
                income=0
            )
            db.session.add(i)
            db.session.commit()
            db.session.refresh(i)
            return AnaliticDto(
                id=i.id, 
                torg=i.torg, 
                body=i.body, worker=i.worker, prom=i.prom, rozet=i.rozet,
                google=i.google_shop, insta=i.insta, profit=i.profit, salary=i.salary, 
                period=i.period, orders=i.orders, inwork=i.inwork,
                stock=i.stock 
                )
        except Exception as e:
            self.logger.error(f'make_row: {e}')
            raise

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
            return True
        except Exception as e:
            self.logger.error(f'add_first: {e}')
            return False


    def load_all(self):
        items = Analitic.query.order_by(
            Analitic.timestamp.desc()
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
    
    def load(self, id):
        try:
            i = Analitic.query.get(id)
            return AnaliticDto(
                id=i.id, torg=i.torg, body=i.body, 
                worker=i.worker, prom=i.prom, rozet=i.rozet,
                google=i.google_shop, insta=i.insta, 
                profit=i.profit, salary=i.salary, 
                inwork=i.inwork, stock=i.stock, 
                period=i.period, orders=i.orders
                )
        except Exception as e:
            self.logger.info(f'repo load: {e}')
            return None

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
        st = start  
        fin = stop
        item = Analitic.query.filter(
            Analitic.timestamp >= st,
            Analitic.timestamp <= fin,
            Analitic.period == period
            ).first()
        print(f'аналітік_реп;', st, fin)
        return item

    def load_period_time_v2(self, period, start, stop):
        try:
            i = Analitic.query.filter(
                Analitic.timestamp >= start,
                Analitic.timestamp <= stop,
                Analitic.period == period
                ).first()
            if not i: return None 
            return AnaliticDto(
                id=i.id, torg=i.torg, body=i.body, 
                worker=i.worker, prom=i.prom, rozet=i.rozet,
                google=i.google_shop, insta=i.insta, 
                profit=i.profit, salary=i.salary, 
                inwork=i.inwork, stock=i.stock, 
                period=i.period, orders=i.orders
                )
        except Exception as e:
            self.logger.exception(f'load_period_time_v2: {e}')
            return None
        
    def load_period_all(self, period, start, stop):
        try:
            items = Analitic.query.filter(
                Analitic.timestamp >= start,
                Analitic.timestamp <= stop,
                Analitic.period == period
                ).all()
            result = []
            for i in items:
                result.append(AnaliticDto(
                    id=i.id, torg=i.torg, body=i.body, 
                    worker=i.worker, prom=i.prom, rozet=i.rozet,
                    google=i.google_shop, insta=i.insta, 
                    profit=i.profit, salary=i.salary, 
                    inwork=i.inwork, stock=i.stock, 
                    period=i.period, orders=i.orders
                    ))
            return result
        except Exception as e:
            if DEBUG>4: print('load_period_all:', e)
            self.logger.exception(f'load_period_all: {e}')
            return None
        
    def update_v2(self, x: AnaliticDto):
        try:
            i = Analitic.query.get_or_404(x.id)
            i.torg = x.torg
            i.body = x.body
            i.worker = x.worker
            i.prom = x.prom
            i.rozet = x.rozet
            i.google_shop = x.google
            i.insta = x.insta
            i.profit = x.profit
            i.period = x.period
            i.orders = x.orders
            i.salary = x.salary
            i.inwork = x.inwork
            i.stock = x.stock
            i.balance = x.balance
            db.session.commit()
            db.session.refresh(i)
            return i
        except Exception as e:
            db.session.rollback()
            self.logger.error(f'update_v2: {e}')
            raise UpdateProblemRepo(f'update_v2')
        
    def update_v3(self, x: AnaliticDto):
        try:
            i = Analitic.query.get_or_404(x.id)
            dto_data = vars(x)

            for field in i.__table__.columns.keys():
                if field in dto_data and field != "id":
                    setattr(i, field, dto_data[field])

            db.session.commit()
            db.session.refresh(i)
            return i
        except Exception as e:
            db.session.rollback()
            self.logger.error(f'update_v2: {e}')
            raise UpdateProblemRepo(f'update_v3')
        
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