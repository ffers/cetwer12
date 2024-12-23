from a_service import prom_serv
from api import prom_api, RozetMain
from .telegram_controller import TelegramController

import sys
sys.path.append('../')
from common_asx.utilits import utils_dev_change


class MarketplaceCntrl:
    def __init__(self, condition):
        self.marketplats = self.init_class(condition)
        self.tg = TelegramController()
    
    def get_orders(self):
        try:
            data = self.marketplats.get_orders()
            if data:
                for order in data["content"]["orders"]:
                    
                    send_tg = self.tg.sendMessage(self.tg.chat_id_confirm, text)
                    resp = self.marketplats.change_status_order(dict_order["id"], 26)
                    print(resp, "status")
                return True
            return False
        except:
            return False
        
    def change_status(self, order_id, status):
        resp =self.marketplats.create_status_get(order_id, status)        
        return resp

    def get_order(self, order_id):
        order_dr = self.marketplats.get_order_id(order_id)
        return order_dr

    def send_ttn(self, order_id, invoice_n, delivery):
        dict_ = prom_serv.dict_invoice(order_id, invoice_n, delivery)
        resp = utils_dev_change.change_ttn(dict_)
        return resp

    def init_class(self, condition):
        if condition == "Rozet":
            return RozetMain()
        elif condition == "Prom":
            return prom_api
        else:
            raise ValueError("Невідомий тип платформи")
        

    def delivery_service_id(self, id):
        if id == 43660: # новапошта
            method = 1
        elif id == 4:
            method = 1
        elif id == 2024:
            method = 1
        elif id == 2:
            method = 1
        elif id == 1:
            method = 1
        else:
            return 1
        return method
    
    def payment_method_id(self, id):
        if id == 5:
            method = 1
        elif id == 4:
            method = 1
        elif id == 3:
            id = 1
        elif id == 2:
            method = 1
        elif id == 1:
            method = 1
        else:
            return print("Нема доступних методів оплати")
        return method
    




