
from utils import DEBUG

from ...base import Handler
from .body import Body

from domain.models.analitic_dto import AnaliticDto

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