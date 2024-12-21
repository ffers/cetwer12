from a_service import prom_serv
from api import prom_api, RozetMain

import sys
sys.path.append('../')
from common_asx.utilits import utils_dev_change


class MarketplaceCntrl:
    def __init__(self, condition):
        self.marketplats = self.init_class(condition)
    
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
        
    def get_orders(self):
        order_dr = self.marketplats.get_orders()
        send_to_crm = order_dr
        return send_to_crm
    




