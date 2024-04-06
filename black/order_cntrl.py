import os, logging, sys
from repository import OrderRep, DeliveryOrderRep
from service_asx.order.telegram.crm_to_telegram import CrmToTelegram
from service_asx.order import ManagerTg, PromToCrm, UpdateToCrm, OrderServ
from service_asx.delivery import NpServ, NpCabinetCl, TTN_to_Prom
from service_asx import DeliveryOrderServ
from api import EvoClient
from dotenv import load_dotenv
from api.nova_poshta.create_data import NpClient
from telegram import TgClient
from black import ProductAnaliticControl





# log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
order_cntrl_handler = logging.FileHandler("../common_asx/log/order_cntrl.log")
order_cntrl_handler.setFormatter(log_formatter)

OC_log = logging.getLogger("order_cntrl")
OC_log.setLevel(logging.INFO)
OC_log.addHandler(order_cntrl_handler)

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
token_ev = os.getenv("PROM_TOKEN")
token_np = os.getenv("NP_TOKEN")
chat_id_helper = os.getenv("CHAT_ID_HELPER")


tg_cl = TgClient()
crmtotg_cl = CrmToTelegram()
ord_rep = OrderRep()
order_prom_serv = PromToCrm()
upd_crm = UpdateToCrm()
tgmn_cl = ManagerTg()
ev_cl = EvoClient(token_ev)
np_cl = NpClient(token_np)
ord_serv = OrderServ()
np_serv = NpServ()
prod_an_cntrl = ProductAnaliticControl()
cab_cl = NpCabinetCl()
ttn_to_prom = TTN_to_Prom()
del_ord_serv = DeliveryOrderServ()
del_ord_rep = DeliveryOrderRep()


class OrderCntrl:
    def load_all_order(self):
        order = ord_rep.load_item_all()
        return order

    def load_confirmed_order(self):
        item = ord_rep.load_for_np()
        print(item)
        return item

    def dublicate(self, order_id):
        item = ord_rep.load_item(order_id)
        dublicate_item = ord_rep.dublicate_item(item)
        ord_prod_old = ord_rep.load_prod_order(order_id)
        dublicate_order_prod = ord_rep.dublicate_order_prod(dublicate_item, ord_prod_old)
        self.add_order_code(dublicate_item)
        return True

    def add_order(self, order):
        data_for_tg = crmtotg_cl.manger(order)
        resp = order_prom_serv.add_order(order, data_for_tg)
        resp_bool = self.examine_address(order)
        return resp

    def examine_address(self, order):
        resp_bool = np_serv.examine_address_prom(order)
        if not resp_bool:
            order_dr = ev_cl.get_order_id(order["id"])
            order = order_dr["order"]
            order_id = order["id"]
            delivery_provider_data = order["delivery_provider_data"]
            try:
                OC_log.info(f"Обробка стандартна, ордер:{order_id}\n Інформація по адресі {delivery_provider_data} ")
                self.update_address(order)
            except:
                tg_cl.send_message_f(chat_id_helper, f"️❗️❗️❗️ Повторно адреси нема в № {order_id} ")
                OC_log.info(f"Обробка ордера: {order_id}\n Інформація по адресі {delivery_provider_data} ")

    def update_address(self, order):
        war_ref = np_serv.examine_address_prom(order)
        # если есть ключ адреса в заказе еще раз додаем адрес,
        # если нет то ето может бить розетка или
        if war_ref:
            if order["delivery_option"]["id"] == 13013934:
                data_address = np_cl.get_s_war_ref(war_ref)
                address_dict_np = np_serv.create_address_dict_np(data_address)
                resp_bool = ord_rep.change_address((order["id"]), address_dict_np)
                return resp_bool
            return True
        OC_log.info(f"Викликаєм помилку {order}")
        raise

    def add_order_code(self, order):
        while True:
            order_code = ord_serv.generate_order_code()
            item = ord_rep.load_for_code(order_code)
            if not item:
                ord_rep.add_order_code(order, order_code)
                return

    def search_for_phone(self, req):
        search_request = req.args.get('q', '').lower()
        print(search_request)
        order = ord_rep.search_for_all(search_request)
        result = ord_serv.search_for_phone(order)
        return result

    def confirmed_order(self, order_id, status):
        order = ord_rep.change_status(order_id, status)
        update_analitic = prod_an_cntrl.product_in_order(order)
        resp = {"success": False}
        if order.delivery_method_id == 1:
            resp = self.work_with_np(order)
            dict_del_ord = del_ord_serv.create_dict(resp, order)
            print(dict_del_ord)
            data_del_ord = del_ord_rep.add_item(dict_del_ord)
        return resp

    def work_with_np(self, order):
        resp = cab_cl.manager_data(
            order)  # обработка зкаказа из срм создание ттн, телеграм курьеру заказ, додавання в пром ттн
        if resp["success"] == True:
            self.await_order_cab_tg(order, "crm_to_telegram")  # if telegram True send to telegram
            invoice_ttn, order_id_sources = ttn_to_prom.main(order)
            ev_cl.make_send_ttn(invoice_ttn, order_id_sources)
        return resp

    def await_order_cab_tg(self, order, flag=None, id=None): # дубль фукціі await_order щоб обійти діспетчер
        print(f"see_flag {flag}")
        resp = None
        if flag == "Надіслати накладну":
            resp = tgmn_cl.send_order_curier(order)
        if flag == "crm_to_telegram":
            resp = tgmn_cl.send(order)
        return resp

    def delete_order(self, id):
        bool = ord_rep.delete_order(id)
        return bool







