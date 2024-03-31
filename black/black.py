import os
from dotenv import load_dotenv
from manager import ManageReg
from service_asx.delivery import ManagerTTN, NpCabinetCl
from service_asx.order import ManagerTg, PromToCrm, UpdateToCrm
from service_asx.delivery import TTN_to_Prom
from service_asx.order.telegram.crm_to_telegram import CrmToTelegram
from api.prom import EvoClient
from repository import OrderRep
from service_asx.order import OrderServ

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
ch_id_sk = os.getenv("CH_ID_SK")
token = os.getenv("PROM_TOKEN")

ord_serv = OrderServ()
ord_rep = OrderRep()
crmtotg_cl = CrmToTelegram()
crm_cl = PromToCrm()
upd_crm = UpdateToCrm()
mng_cl = ManagerTTN()
mreg_cl = ManageReg()
tgmn_cl = ManagerTg()
cab_cl = NpCabinetCl()
ttn_to_prom = TTN_to_Prom()
ev_cl = EvoClient(token)

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

    def await_cabinet(self, order_id, status):
        order = ord_rep.change_status(order_id, status)
        resp = {"success": False}
        if order.delivery_method_id == 1:
            resp = self.work_with_np(order)
        return resp


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

    def work_with_np(self, order):
        resp = cab_cl.manager_data(
            order)  # обработка зкаказа из срм создание ттн, телеграм курьеру заказ, додавання в пром ттн
        if resp["success"] == True:
            self.await_order_cab_tg(order, "crm_to_telegram")  # if telegram True send to telegram
            invoice_ttn, order_id_sources = ttn_to_prom.main(order)
            ev_cl.make_send_ttn(invoice_ttn, order_id_sources)
        return resp





