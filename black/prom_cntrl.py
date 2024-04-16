from a_service import prom_serv
from api import prom_api


class PromCntrl:
    def change_status(self, order_id, status):
        dict_status = prom_serv.create_status_get(order_id, status)
        prom_api.get_set_status(dict_status)

    def get_order(self, order_id):
        order_dr = prom_api.get_order_id(order_id)
        return order_dr

prom_cntrl = PromCntrl()
