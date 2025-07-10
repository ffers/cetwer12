



import os
from utils import DEBUG
from ..base import Handler

from domain.models import AnaliticDto

class Periodtodel(Handler):
    def process(self, day, period_flag):
        try:
            # periods = ['week', 'month', 'year', 'all']
            # for p in periods:
            day = self.make_day(day)
            row = self.make_period_rows(period_flag)
            return self.count_v2(day, row, period_flag)     
        except Exception as e:
            print('Помилка')
            if DEBUG > 1: print(e)  
            self.ctx.logger.exception(f'Period_process - {e}')

    def make_period_rows(self, period_flag):
        start_time, stop_time = self.ctx.w_time.load_work_time(period_flag)
        rows = self.return_row(period_flag, start_time, stop_time)
        print('time:', start_time, stop_time)
        if DEBUG>5: print('an_rows:', rows)
        return rows
    
    def make_day(self, day):
        start_time, stop_time = self.ctx.w_time.day()
        an_row = self.return_row(day, start_time, stop_time)
        print('time:', start_time, stop_time)
        if DEBUG>5: print('an_row:', an_row)
        return an_row

    def count_v2(self, day, period, per_flag):
        count = self.count(day, period, per_flag)
        print('sum_row:', count)
        resp = self.ctx.an_rep.update_v3(count)
        return resp
    
    def return_row(self, period, start_time, stop_time):
        row = self.ctx.an_rep.load_period_time_v2(period, start_time, stop_time)
        if not row:
            row = self.ctx.an_rep.add_row(period, start_time) 
        return row
    
    def count(self, day: AnaliticDto, period: AnaliticDto, per_flag):
        try:
            period.orders += day.orders
            period.torg += day.torg
            period.body += day.body
            period.worker += day.worker
            period.profit += day.profit
            period.prom += day.prom
            period.rozet += day.rozet
            period.salary += day.salary
            period.balance = day.balance
            period.wait = day.wait
            period.stock = day.stock
            period.inwork = day.inwork
            period.income = day.income
            print(f"новий кеш: {period}")
            return period
        except Exception as e:
            self.ctx.logger.exception(f'count: {e}')
            raise