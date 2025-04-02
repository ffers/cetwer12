from a_service import prom_serv
from api import prom_api
import sys, os, re
sys.path.append('../')
from api import EvoClient, RozetMain
from common_asx.utilits import Utils


class PromCntrl:
    def send_ttn(self, order_id, invoice_n, delivery):
        order_id = re.sub(r"\D", "", order_id)
        env =os.getenv("ENV")
        if env != "dev":
            token = os.getenv("PROM_TOKEN")
            evo_cl = EvoClient(token)
            resp = evo_cl.send_ttn(order_id, invoice_n, delivery)
            return resp
        return {"success": "dev"}
    
    def change_status(self, order_id, status):
        order_id = re.sub(r"\D", "", order_id)
        env =os.getenv("ENV")
        if env != "dev":
            token = os.getenv("PROM_TOKEN")
            evo_cl = EvoClient(token)
            resp = evo_cl.change_status(order_id, status)
            return resp
        return {"success": "dev"}

    def get_order(self, order_id):
        order_dr = prom_api.get_order_id(order_id)
        return order_dr


prom_cntrl = PromCntrl()
