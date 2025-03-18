from a_service import prom_serv
from api import prom_api
import sys
sys.path.append('../')
from api import EvoClient, RozetMain
from common_asx.utilits import Utils


class PromCntrl:
    def change_status(self, order_id, status):
        dict_status = prom_serv.create_status_get(order_id, status)
        # prom_api.get_set_status(dict_status)
        resp = Utils(EvoClient, RozetMain).change_status(dict_status)
        return resp


    def get_order(self, order_id):
        order_dr = prom_api.get_order_id(order_id)
        return order_dr

    def send_ttn(self, order_id, invoice_n, delivery):
        dict_ = prom_serv.dict_invoice(order_id, invoice_n, delivery)
        resp = Utils(EvoClient, RozetMain).change_ttn(dict_)
        return resp

prom_cntrl = PromCntrl()
