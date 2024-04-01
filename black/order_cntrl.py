import os, logging, sys
from repository import OrderRep
from service_asx.order.telegram.crm_to_telegram import CrmToTelegram
from service_asx.order import ManagerTg, PromToCrm, UpdateToCrm, OrderServ
from service_asx.delivery import NpServ
from api import EvoClient
from dotenv import load_dotenv
from api.nova_poshta.create_data import NpClient
from telegram import TgClient

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
crm_cl = PromToCrm()
upd_crm = UpdateToCrm()
tgmn_cl = ManagerTg()
ev_cl = EvoClient(token_ev)
np_cl = NpClient(token_np)
ord_serv = OrderServ()
np_serv = NpServ()

class OrderCntrl:
    def dublicate(self, order_id):
        item = ord_rep.load_item(order_id)
        dublicate_item = ord_rep.dublicate_item(item)
        ord_prod_old = ord_rep.load_prod_order(order_id)
        dublicate_order_prod = ord_rep.dublicate_order_prod(dublicate_item, ord_prod_old)
        self.add_order_code(dublicate_item)
        return True

    def add_order(self, order):
        data_for_tg = crmtotg_cl.manger(order)
        resp = crm_cl.add_order(order, data_for_tg)
        resp_bool = self.examine_address(order)
        return resp

    def examine_address(self, order):
        resp_bool = np_serv.examine_address_prom(order)
        if not resp_bool:
            order_dr = ev_cl.get_order_id(order["id"])
            order = order_dr["order"]
            order_id = order["id"]
            delivery_provider_data = order["delivery_provider_data"]
            # try:
            self.update_address(order)
            # except:
            #     tg_cl.send_message_f(chat_id_helper, f"️❗️❗️❗️ Повторно адреси нема в № {order_id} ")
            #     OC_log.info(f"Обробка ордера: {order_id}\n Інформація по адресі {delivery_provider_data} ")

    def update_address(self, order):
        war_ref = np_serv.examine_address_prom(order)
        # если есть ключ адреса в заказе еще раз додаем адрес,
        # если нет то ето может бить розетка или
        if war_ref:
            if order["delivery_option"]["id"] == 13013934:
                data_address = np_cl.get_s_war_ref(war_ref)
                address_dict_np = np_serv.create_address_dict_np(data_address)
                resp_bool = ord_rep.change_address(order["id"], address_dict_np)
                return resp_bool
            return True
        raise

    def add_order_code(self, order):
        while True:
            order_code = ord_serv.generate_order_code()
            item = ord_rep.load_for_code(order_code)
            if not item:
                ord_rep.add_order_code(order, order_code)
                return








