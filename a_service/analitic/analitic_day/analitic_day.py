from utils import DEBUG
from dataclasses import asdict


from ..base import Handler
from .handlers.body import Body
from domain.models.analitic_dto import AnaliticDto
from domain.models import BalanceDTO
from decimal import Decimal

class OrderHaveSendTime(Exception):
    pass
class StockOrderHaventComps(Exception):
    pass


    pass

class CountAnaliticV2(Handler):
    def day(self): 
        #self.sort_send_time() # проверка на компонеенти и добавление времени отправки (в чем нет нееобхожимости когда будет закгрузка по статусу) /
        # также отметка времени отправки
        start_time, stop_time = self.ctx.w_time.day()
        # перевіряєм чи за цеей період данні в аналітиці
        # item = an_cntrl.load_period_sec(period, start_time, stop_time)
        # якщо є треба додати до цього новий підрахунок якщо він є /
        # якщо нема рахувати з нуля
        self.ctx.logger.debug(f"period: {start_time, stop_time}")
        resp =CheckConfirmedOrder(self.ctx).process()

'остановился на загрузке ордеров и решение как сортировать их'

class CheckConfirmedOrder(Handler):
    def process(self):
        logger = self.ctx.logger
        orders = self.ctx.ord_rep.load_send()
        for order in orders:
            try:
                self.check(order)
            except OrderHaveSendTime:
                logger.error(
                   f"order without with send_time: {order.id}") 
                pass
            except Exception as e:
                self.ctx.logger.error(
                   f"CheckConfirmedOrder: {e}") 
                raise
        return orders
    
    def check(self, order):
        if order.send_time:
            raise OrderHaveSendTime('Цей ордер вже має час відправки')
        else:
            return AnaliticDay(self.ctx).process(order)
 

    def fixed_journal_and_stock(self):
        pass

'Аналітика на день'
class AnaliticDay(Handler):
    def process(self, order):
        return self.make_day(order)

    def make_day(self, order):
        start_time, stop_time = self.ctx.w_time.day()
        an_row = self.return_row(start_time, stop_time)
        print('time:', start_time, stop_time)
        if DEBUG>5: print('an_row:', an_row)
        
        count = self.count(order, an_row)
        print('sum_row:', count)
        resp = self.ctx.an_rep.update_v3(count)
        update_order = self.update_order(order)
        return resp

        
    def return_row(self, start_time, stop_time):
        row = self.ctx.an_rep.load_period_time_v2('day', start_time, stop_time)
        if not row:
            row = self.ctx.an_rep.add_row('day', start_time) 
        return row
    
    def count(self, order, x: AnaliticDto):
        count = Count(self.ctx) # пока незнаю как назвать 
        wait = Wait(self.ctx)
        stock = Stock(self.ctx)
        balance = Balance(self.ctx)
        inwork = Inwork(self.ctx)
        try:
            stock_sum = stock.process(order)
            torg = count.torg_func(order)
            x.stock = stock_sum
            x.orders += 1
            x.torg += torg
            x.body += count.body_v2(order)
            x.worker += 27
            x.profit += x.torg - x.body
            x.prom += count.cpa_com_f(order)
            x.rozet += count.rozet_f(order)
            x.period = 'day'
            x.salary = count.salary(x)
            x.balance = balance.process()
            x.wait = wait.wait(torg)
            x.inwork = inwork.process()
            print(f"новий кеш: {x}")
            return x
        except Exception as e:
            self.ctx.logger.exception(f'count: {e}')
            raise
    
    # def sum_row(self, x: "AnaliticDto", y: "AnaliticDto") -> "AnaliticDto":
    #     try:
    #         print('sum_row', x.salary, y.salary)
    #         return AnaliticDto(
    #             id=x.id,
    #             torg=x.torg + y.torg,
    #             body=x.body + y.body,
    #             workers=x.workers + y.workers,
    #             prom=x.prom + y.prom,
    #             rozet=x.rozet + y.rozet,
    #             google=x.google + y.google,
    #             insta=x.insta + y.insta,
    #             profit=x.profit + y.profit,
    #             orders=x.orders + y.orders,
    #             period=x.period,
    #             salary=x.salary + y.salary,
                
    #         )
    #     except Exception as e:
    #         if DEBUG > 2: self.ctx.logger.exception(f'count: {e}')
    #         raise

    def add_to_all(self, all, new_day):
        return all + new_day
    
    def update_order(self, order):
        try:
            self.ctx.ord_rep.update_time_send(order.id, next(self.ctx.w_time.my_time()))
            return True
        except Exception as e:
            self.ctx.logger.error(f'update_order {order.id} cant update: {e}')
            raise 

        

class Count(Handler):
    def torg(self, product):
        torg = 0
        if product.quantity and product.price:
            torg = product.quantity * product.price
        return torg

    def torg_func(self, order):
        torg = 0
        for product in order.ordered_product:
            torg += self.torg(product)
        return torg
    
    def body_v2(self, order):
        count = Body(self.ctx)
        return count.process(order)
    
    def cpa_com_f(self, order):
        cpa_commission = 0
        if DEBUG > 4: print('cpa_com_f:', order.cpa_commission)
        if order.cpa_commission:
            cpa_commission += self.format_float(order.cpa_commission)
        return cpa_commission
    
    def rozet_f(self, order):
        rozet = 0
        if order.delivery_method_id == 2:
            print(order.delivery_method.name)
            rozet += 30
        return rozet
    
    def salary(self, x: AnaliticDto):
        return x.profit - x.worker - x.prom - x.rozet - x.google - x.insta

    def inwork(self, x: AnaliticDto):
        return x.stock + x.inwork + x.balance
    
class Wait(Handler):
    def wait(self, torg):
        balance = self.ctx.balance_rep.get(2)
        balance.wait += torg
        balance = self.ctx.balance_rep.update_wait(balance)
        return balance.wait
    
    def wait_update(self, torg):
        try:
            balance = self.ctx.balance_rep.get(2)
            balance.wait += torg
            balance = self.ctx.balance_rep.update_wait(balance)
        except Exception as e:
            self.ctx.logger.exception(f'Wait: {e}')
            raise

class Stock(Handler):
    def process(self, order):
        try:
            self.check(order)
            money = self.count()
            self.update(money)
            return money
        except Exception as e:
            self.ctx.logger.error(f'Stock process: {e}')
            raise

    def check(self, order):
        resp = self.ctx.source_an_cntrl.prod_component_process(order, 'confirmed')
        if not resp:
            raise StockOrderHaventComps('Нема компонентів')

    def count(self):
        money = Decimal('0.00')
        items = self.ctx.source_rep.load_all()
        for item in items:
            money += item.money
        print('stock:', money)
        return money
    
    def update(self, money):
        balance = self.ctx.balance_rep.get(2)
        balance.stock = money
        self.ctx.balance_rep.update_stock(balance)
        
class Inwork(Handler):
    def process(self):
        try:
            balance = self.ctx.balance_rep.get(2)
            balance.inwork = balance.stock + balance.wait + balance.balance
            self.ctx.balance_rep.update_inwork(balance)
            return balance.inwork
        except Exception as e:
            self.ctx.logger.error(f'Inwork process: {e}')
            raise

class Balance(Handler):
    def process(self):
        balance = self.ctx.balance_rep.get(2)
        return balance.balance





