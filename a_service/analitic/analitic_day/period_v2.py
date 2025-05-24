



import os
from utils import DEBUG
from ..base import Handler

from domain.models import AnaliticDto

class DontHaveAnaliticData(Exception):
    pass

class PeriodV2(Handler):
    def process(self, item_flag, period_flag):
        try:
            # periods = ['week', 'month', 'year', 'all']
            # for p in periods:
            item = self.return_item(item_flag)
            if DEBUG>4: print('return_item:', item_flag)
            period = self.return_period(item_flag, period_flag)
            if DEBUG>4: print('return_period:', period)
            return self.count_v2(item, period)     
        except Exception as e:
            print('Помилка')
            if DEBUG > 1: print(e)  
            self.ctx.logger.exception(f'Period_process - {e}')
            raise

    def return_item(self, item_flag):
        start_time, stop_time = self.ctx.w_time.load_work_time(item_flag)
        if DEBUG>4: print('return_item:', start_time, stop_time)
        row = self.ctx.an_rep.load_period_time_v2(item_flag, start_time, stop_time)
        if DEBUG>4: print('return_item:', row)
        if not row:
            row = self.ctx.an_rep.add_row(item_flag, start_time) 
        return row
    
    def return_period(self, item_flag, period_flag):
        start_time, stop_time = self.ctx.w_time.load_work_time(item_flag)
        if DEBUG>4: print('return_period:', start_time, stop_time)
        p = self.ctx.an_rep.load_period_all(period_flag, start_time, stop_time)
        if DEBUG>4: print('return_period:', p)
        if not p:
            raise DontHaveAnaliticData('Немає ще данних для підрахунку')
        return p
    
    def count_v2(self, item: AnaliticDto, period: list[AnaliticDto]):
        item = self.make_zero(item)
        item = self.balance(item)
        for p in period:
            item = self.count(item, p)
        if DEBUG>4:print('sum_row:', item)
        resp = self.ctx.an_rep.update_v3(item)
        return resp
    
    def count(self, item: AnaliticDto, p: AnaliticDto):
        try:
            item.orders += p.orders
            item.torg += p.torg
            item.body += p.body
            item.worker += p.worker
            item.profit += p.profit
            item.prom += p.prom
            item.rozet += p.rozet
            item.salary += p.salary
            if DEBUG>4:print(f"новий кеш: {item}")
            return item
        except Exception as e:
            self.ctx.logger.exception(f'count: {e}')
            raise

    def make_zero(self, item):
        return AnaliticDto(id=item.id, period=item.period)
    
    def balance(self, item):
        p = self.ctx.balance_rep.get(2)
        item.balance = p.balance
        item.wait = p.wait
        item.stock = p.stock
        item.inwork = p.inwork
        return item
