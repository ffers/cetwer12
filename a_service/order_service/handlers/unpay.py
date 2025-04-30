

from utils import OC_logger
from ..order_api_process import OrderApi
from repository import OrderRep
from mapper import promMapper
from a_service.product_serv import ProductServ
from a_service.telegram_service import TgServNew
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


class Handler:
    def __init__(
            self, 
            store_data, 
            token, 
            EvoClient, 
            RozetMain, 
            Repo: OrderRep,
            TgServNew: TgServNew
            ):
        self.repo = Repo()
        self.store = OrderApi(store_data.api, token, EvoClient, RozetMain)
        self.tg = TgServNew
        self.logger = OC_logger.oc_log('order_serv')
        self.store_id = store_data.id
        

    def execute(self, data):
        pass

class GetOrderStore(Handler):
    def execute(self, order):
        self.logger.info(f'Перевіряємо замовлення: {order.order_code}')
        order_store = self.store.get_order(order.order_code)
        return self.order_mapper(order_store, order)

    def order_mapper(self, order_store, order):
        order_store = promMapper(order_store, ProductServ, self.store_id)
        if not order_store:
            self.logger.error(f'Такого ордера нема: {order.order_code}')
            raise OrderNotFoundException(f'Order not found in store: {order.order_code}')
        elif order_store.payment_status_id == 1:
            self.logger.info(f'Цей ордер оплачено: {order.order_code}')
            return True
        else:
            self.logger.info(f'Цей ордер ще не оплачено: {order.order_code}')
            raise OrderNotPaidException(f'Order not paid: {order.order_code}')
        
        
class ChangeOrder(Handler):
    def execute(self, order):
        resp = self.repo.update_payment_status(order.id, 1)
        if not resp:
            self.logger.error(f'Помилка зміни статусу: {order.order_code}')
            raise OrderNotUpdateStatusException(f'Помилка зміни статусу {order.order_code}') # щось інше треба відповісти
        return resp

class SendManager(Handler):
    def execute(self, order):
        resp = self.tg.sendMessage(self.tg.chat_id_confirm, f'Оплачeно замовлення {order.order_code}')
        if not resp:
            self.logger.error(f'Помилка відправкі менеджеру: {order.order_code}')
            raise TGsendMessageException(f'Помилка відправкі менеджеру {order.order_code}')
        return True
        
class Unpay:
    def __init__(self):
        self.commands = [
            GetOrderStore,
            ChangeOrder,
            SendManager 
            ]

    def add_command(self, command_class):
        self.commands.append(command_class)
        return self

    def build(self, order, store_data, token, EvoClient, RozetMain, Repo, TGServ):  
            for cmd_class in self.commands:
                print("Працює: ", cmd_class.__name__)
                pointer = cmd_class(store_data, token, EvoClient, RozetMain, Repo, TGServ).execute(order)
            return pointer