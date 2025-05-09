

from utils import OC_logger
from ...order_api_process import OrderApi
from repository import OrderRep
from mapper import promMapper
from a_service.product_serv import ProductServ
from a_service.telegram_service import TgServNew
from ..base import Handler, UnpayContext
from exceptions.order_exception import *

'''
status оплати за яким принципом відслідковувати
Замовленя нове, або редагування 
Замовленя має оплату пром
статус оплати не сплачено
завантажити несплачені ордери за певвний період по пром
перевірити по ним оплату в пром якщо оплачено 
змінти статус оплати на Оплачено 
повідомити менеджераза
'''

'''
Питання по пром токен 
якщо замовленя віда треба це знати, 
ввикористовувати окреему таблицю для позначення
звідки ордер
ордер має источник 
прописувати ордеру з якого конкретно стора 
'''



class TGsendMessageException(Exception):
    pass

class GetApi(Handler):
    def execute(self, order):
        api = self.ctx.state.store.api
        apis = {
                "rozetka": self.ctx.roz_serv,
                "prom": self.ctx.evo_serv
        }
        if api in apis:
            self.ctx.state.store_api = apis[api]
        else:
            raise ValueError(f"We dont have api: {api}")  

class GetOrderStore(Handler):
    def execute(self, order):
        self.logger.info(f'Перевіряємо замовлення: {order.order_code}')
        order_store = self.ctx.state.store_api.get_order(order.order_code)
        return self.order_mapper(order_store, order)

    def order_mapper(self, order_store, order):
        store_id = self.ctx.state.store.id
        order_store = promMapper(order_store, ProductServ, store_id)
        if not order_store:
            raise OrderNotFoundException(f'Order not found in store: {order.order_code}')
        elif order_store.payment_status_id == 1:
            self.logger.info(f'Цей ордер оплачено: {order.order_code}')
            return True
        else:
            raise OrderNotPaidException(f'Order not paid: {order.order_code}')
        
        
class ChangeOrder(Handler):
    def execute(self, order):
        resp = self.ctx.order_repo.update_payment_status(order.id, 1)
        if not resp:
            raise OrderNotUpdateStatusException(f'Помилка зміни статусу {order.order_code}') # щось інше треба відповісти
        return resp

class SendManager(Handler):
    def execute(self, order):
        resp = self.ctx.tg_serv.sendMessage(self.ctx.tg_serv.chat_id_confirm, f'Оплачeно замовлення {order.order_code}')
        if not resp:
            raise TGsendMessageException(f'Помилка відправкі менеджеру {order.order_code}')
        return True
        
class ValidateUnpayOrderHandler:
    def __init__(self, ctx):
        self.logger = OC_logger.oc_log('order_serv.handler.unpay_work')
        self.ctx = ctx
        self.commands = [
            GetApi,
            GetOrderStore,
            ChangeOrder,
            SendManager
        ]

    def handle(self, order):
        for cmd_class in self.commands:
            self.logger.debug(f"Працює: {cmd_class.__name__}")
            cmd_class(self.ctx).execute(order)
        return f'Оплачено: {order.order_code}'


class OrderProcessor:
    def __init__(self, handler: ValidateUnpayOrderHandler):
        self.handler = handler
        self.logger = OC_logger.oc_log('unpay_work.order_prrocessor')

    def handle_all(self, orders):
        results = []
        
        for order in orders:
            try:
                result = self.handler.handle(order)
                results.append(result)
            except Exception as e:
                self.logger.debug(f'ордер {order.order_code} ще неоплачено: {e}')
        return results

    
