from .base import Handler, Context
from utils import OC_logger


class OrderHaveSendTime(Exception):
    pass

class CountAnaliticV2(Handler):
    def __init__(self):
        pass
    # def count(self):
    #     days = 
    #     week = 
    #     month
    #     yar
    #     all_time 

    def day(self):
        self.sort_send_time()
        start_time, stop_time = self.w_time.day()
        self.logger.debug(f"period: {start_time, stop_time}")
        orders = CheckConfirmedOrder().process()
        

'остановился на загрузке ордеров и решение как сортировать их'

class CheckConfirmedOrder(Handler):
    def process(self):
        orders = self.ord_rep.load_send()
        for order in orders:
            try:
                self.check(order)
            except OrderHaveSendTime:
               self.logger.error(
                   f"order without with send_time: {order.id}") 
            except Exception as e:
                self.logger.error(
                   f"CheckConfirmedOrder: {e}") 

    
    def check(self, order):
        if order.send_time:
            raise 
            print("Щось оновлено")
            confirmed = self.confirmed(order)
            if confirmed:
                self.ord_rep.update_time_send(order.id, next(self.my_time()))
        return resp


'Аналітика на день'
class AnaliticDay:
    def __init__(self):
        pass

    def make_day(self):
        pass

    def count_day(self, take_cash):
        pass

    def add_to_all(self, all, new_day):
        return all + new_day


    def minus_old_day(self, all, old_day):
        pass