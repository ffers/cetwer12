import os
from dotenv import load_dotenv
from .manager_ttn import ManagerTTN
from service_asx.order import ManagerTg, PromToCrm, UpdateToCrm
from service_asx.order.telegram.crm_to_telegram import CrmToTelegram
from repository import OrderRep
from service_asx.order import OrderServ
from .product_analitic_cntrl import ProductAnaliticControl


env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
ch_id_sk = os.getenv("CH_ID_SK")

ord_serv = OrderServ()
ord_rep = OrderRep()
crmtotg_cl = CrmToTelegram()
crm_cl = PromToCrm()
upd_crm = UpdateToCrm()
mng_cl = ManagerTTN()
tgmn_cl = ManagerTg()
prod_an_cntrl = ProductAnaliticControl()

class Await:
    def await_order(self, order, flag=None, id=None):
        print(f"ДИвимось флаг {flag}")
        resp = None
        if flag == "prom_to_crm":
            data_for_tg = crmtotg_cl.manger(order)
            resp = crm_cl.add_order(order, data_for_tg)
        if flag == "update_to_crm":
            resp = upd_crm.manager(order)
        else:
            tgmn_cl.see_flag(order, flag)
        return resp

    def await_interface(self, order_id):
        ttn_data = mng_cl.create_ttn(order_id)
        resp_ok = mng_cl.add_ttn_crm(order_id, ttn_data)
        return ttn_data

    def await_cabinet_json(self, data):
        if "search_city" in data["name"]:
            pass

    def await_order_cab_tg(self, order, flag=None, id=None): # дубль фукціі await_order щоб обійти діспетчер
        print(f"see_flag {flag}")
        resp = None
        if flag == "Надіслати накладну":
            resp = tgmn_cl.send_order_curier(order)
        if flag == "crm_to_telegram":
            resp = tgmn_cl.send(order)
        return resp







