import os, logging, sys
from repository import OrderRep
from black.crm_to_telegram import CrmToTelegram
from a_service.order import  OrderServ
from a_service.delivery import NpServ
from a_service import DeliveryOrderServ
from dotenv import load_dotenv
from api.nova_poshta.create_data import NpClient
from .telegram_controller import tg_cntrl
from .np_cntrl import NpCntrl
from .product_analitic_cntrl import ProductAnaliticControl
from .delivery_order_cntrl import DeliveryOrderCntrl
from .add_order_to_crm import pr_to_crm_cntr
from a_service import tg_serv
from .prom_cntrl import prom_cntrl
from utils import util_asx
from .sour_an_cntrl import sour_an_cntrl
from datetime import datetime

sys.path.append('../')
from common_asx.utilits import Utils

# log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
token_ev = os.getenv("PROM_TOKEN")
token_np = os.getenv("NP_TOKEN")
chat_id_helper = os.getenv("CHAT_ID_HELPER")

OC_log = util_asx.oc_log("order_cntrl_test")


crmtotg_cl = CrmToTelegram()
ord_rep = OrderRep()


np_cl = NpClient(token_np)
ord_serv = OrderServ()
np_serv = NpServ()
prod_an_cntrl = ProductAnaliticControl()
np_cntrl = NpCntrl()
del_ord_serv = DeliveryOrderServ()
del_ord_cntrl = DeliveryOrderCntrl()
util_cntrl = Utils()


class OrderCntrl:
    def my_time(self):
        yield (datetime.now())

    def load_all_order(self):
        order = ord_rep.load_item_all()
        return order

    def load_confirmed_order(self):
        item = ord_rep.load_for_np()
        return item

    def load_registred(self):
        item = ord_rep.load_registred()
        print(item)
        return item

    def load_registred_roz(self):
        item = ord_rep.load_registred_roz()
        print(item)
        return item

    def load_status_id(self, id):
        return ord_rep.load_status_id(id)

    def load_order_for_code(self, order_code):
        order = ord_rep.load_for_code(order_code)
        return order.id

    def load_for_order_code(self, order_code):
        order = ord_rep.load_for_order_code(order_code)
        return order

    def dublicate(self, order_id):
        item = ord_rep.load_item(order_id)
        dublicate_item = ord_rep.dublicate_item(item)
        ord_prod_old = ord_rep.load_prod_order(order_id)
        dublicate_order_prod = ord_rep.dublicate_order_prod(dublicate_item, ord_prod_old)
        self.add_order_code(dublicate_item)
        self.send_order_tg(dublicate_item.id)
        return True

    def add_order(self, order_js):
        order_code = order_js["id"]
        try:
            data_for_tg = crmtotg_cl.manger(order_js)
            resp = pr_to_crm_cntr.add_order(order_js, data_for_tg)
            print(order_js)
            order = ord_rep.load_for_code(order_js["id"])
            print(f"add_order {order.id}")
            bool_1 = del_ord_cntrl.add_item(order.id, 1)
            bool_2 = self.examine_address(order_js)
            return resp
        except:
            info = f"Замовленя можливо не додано в CRM {order_code}"
            OC_log.info(info)
            tg_cntrl.sendMessage(tg_cntrl.chat_id_confirm, info)

    def examine_address(self, order):
        resp_bool = np_serv.examine_address_prom(order)
        if not resp_bool:
            order_dr = prom_cntrl.get_order(order["id"])
            order = order_dr["order"]
            order_id = order["id"]
            delivery_provider_data = order["delivery_provider_data"]
            try:
                OC_log.info(f"Обробка стандартна, ордер:{order_id}\n Інформація по адресі {delivery_provider_data} ")
                tg_cntrl.send_message_f(chat_id_helper,
                                     f"Обробка стандартна, ордер:{order_id}\n Інформація по адресі {delivery_provider_data} ")
                self.update_address(order)
            except:
                tg_cntrl.send_message_f(chat_id_helper,
                                f"️❗️❗️❗️ Повторно адреси нема в № {order_id} ")
                OC_log.info(
                    f"Обробка ордера: {order_id}\n "
                    f"Інформація по адресі {delivery_provider_data} ")

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

    def send_order_tg(self, order_id):
        order = ord_rep.load_item(order_id)
        data_tg_dict = tg_serv.create_text_order(order)
        keyboard_json = tg_cntrl.keyboard_func()
        resp = tg_cntrl.sendMessage(tg_cntrl.chat_id_confirm, data_tg_dict, keyboard_json)
        return True


    def search_for_phone(self, req):
        search_request = req.args.get('q', '').lower()
        print(search_request)
        order = ord_rep.search_for_all(search_request)
        result = ord_serv.search_for_order(order)
        return result

    def confirmed_order(self, order_id):
        print("first")
        order = ord_rep.load_item(order_id)
        crm_status = ord_rep.change_status(order_id, 2)
        bool_prom = self.definition_source(order, 3)
        update_analitic = prod_an_cntrl.product_in_order(order)

        delivery = self.check_del_method(order)
        result = self.result(crm_status, bool_prom,
                             update_analitic, delivery)

        resp_tg = tg_cntrl.sendMessage(tg_cntrl.chat_id_confirm, "{ordered_status} {order_code}".format(**crm_status))
        return result

    def result(self, *args):
        result = {
            "crm_status": args[0],
            "bool_prom": args[1],
            "update_analitic": args[2],
            "delivery": args[3]
        }
        return result

    def question_order(self, order_id):
        order = ord_rep.load_item(order_id)
        bool = self.change_status_item(order_id, 5)
        bool_prom = self.definition_source(order, 2)
        return bool

    def definition_source(self, order, status):
        bool_prom = True
        if order.source_order_id == 2:
            bool_prom = prom_cntrl.change_status(order.order_code, status)
        return bool_prom

    def return_order(self, order_id, status):
        order = ord_rep.load_item(order_id)
        bool = ord_rep.change_status(order_id, status)
        bool_prom = prom_cntrl.change_status(order_id, 2)
        # update_analitic = prod_an_cntrl.product_in_order(order)
        resp_sour = sour_an_cntrl.return_prod(order)
        # resp = self.check_del_method(order)
        return bool

    def send_storage(self, order_id):
        order = ord_rep.load_item(order_id)
        resp_sour = sour_an_cntrl.confirmed(order)
        return resp_sour

    def check_del_method(self, order):
        resp = False
        print("deliveri method", order.delivery_method_id)
        if order.delivery_method_id == 1:
            resp = self.del_method_np(order)
        elif order.delivery_method_id == 2 or order.delivery_method_id == 4:
            print("Розетка")
            resp = self.del_method_roz(order)
        elif order.delivery_method_id == 3:
            resp = self.del_method_ukr(order)
        elif order.delivery_method_id == 5:
            resp = self.del_method_shop(order)
        return resp

    def del_method_np(self, order):
        resp = False
        np_resp = np_cntrl.manager_data(
            order)  # обработка зкаказа из срм создание ттн, телеграм курьеру заказ, додавання в пром ттн
        if np_resp["success"] == True:
            doc_ttn = np_resp["data"][0]["IntDocNumber"]
            resp_ttn = self.add_ttn_crm(order.id, doc_ttn)
            order = ord_rep.load_item(order.id)
            data_tg_dict = tg_serv.create_text_order(order)  # if telegram True send to telegram
            tg_cntrl.sendMessage(tg_cntrl.chat_id_np, data_tg_dict)
            del_ord_cntrl.update_item(np_resp, order.id)
            resp = True, ""
            if order.source_order_id == 2:
                resp_prom_ttn = prom_cntrl.send_ttn(order.order_code, order.ttn, "nova_poshta")
                resp_prom_status = prom_cntrl.change_status(order.order_code, 137639)
        elif 'OptionsSeat is empty' in np_resp["errors"]:
            resp = "Поштомат зайнятий"
            tg_cntrl.sendMessage(tg_cntrl.chat_id_confirm,
                                 "❗️❗️❗️ ТТН не створено - поштомат зайнятий")
        else:
            resp = False, np_resp["errors"]
            tg_cntrl.sendMessage(tg_cntrl.chat_id_confirm,
                                 f"❗️❗️❗️ ТТН не створено - {resp[1]}")
        return resp

    def add_ttn_crm(self, order_id, ttn):
        resp = ord_rep.add_ttn_crm(order_id, ttn)
        return resp

    def del_method_roz(self, order):
        data_tg_dict = tg_serv.create_text_order(order)
        print(f"data_tg_dict {data_tg_dict}" )
        print(order.order_code)
        # tg_cntrl.answerCallbackQuery(callback_query_id, f"Відсилаю в Розетку")
        keyboard_rozet = tg_cntrl.keyboard_generate("Надіслати накладну", order.order_code)
        resp = tg_cntrl.sendMessage(tg_cntrl.chat_id_rozet, data_tg_dict, keyboard_rozet)
        print(resp)
        return True

    def del_method_ukr(self, order):
        print("Відсилаю в Укрпошту")
        data_tg_dict = tg_serv.create_text_order(order)
        # tg_cntrl.answerCallbackQuery(callback_query_id, f"Відсилаю в Розетку")
        # keyboard_rozet = tg_cntrl.keyboard_generate("Надіслати накладну", order.order_code)
        resp = tg_cntrl.sendMessage(tg_cntrl.chat_id_ukr, data_tg_dict)
        return True

    def del_method_shop(self, order):
        print("Відсилаю в Шопзаказ")
        data_tg_dict = tg_serv.create_text_order(order)
        # tg_cntrl.answerCallbackQuery(callback_query_id, f"Відсилаю в Розетку")
        # keyboard_rozet = tg_cntrl.keyboard_generate("Надіслати накладну", order.order_code)
        resp = tg_cntrl.sendMessage(tg_cntrl.chat_id_shop, data_tg_dict)
        return True

    def await_order_cab_tg(self, order, flag=None, id=None): # дубль фукціі await_order щоб обійти діспетчер
        print(f"see_flag {flag}")
        resp = None
        if flag == "Надіслати накладну":
            resp = tg_serv.send_order_curier(order)
        if flag == "crm_to_telegram":
            resp = tg_serv.create_text_order(order)
        return resp

    def delete_order(self, id):
        print(f"delete order {id}")
        bool = ord_rep.delete_order(id)
        return bool

    def change_status(self, data):
        orders, status = ord_serv.parse_dict_status(data)
        print("WTF")
        for order in orders:
            print (f"%s %s try change" % (order, status))
            self.change_status_item(order, status)
        # bool = ord_rep.change_status_list(orders, status)
        return True

    def change_status_item(self, id, status):
        resp = ord_rep.change_status(id, status)
        resp_tg = tg_cntrl.sendMessage(tg_cntrl.chat_id_confirm, "{ordered_status} {order_code}".format(**resp))
        print(resp_tg)
        return resp.update( {"message_id": resp_tg["result"]["message_id"]})

    def change_status_roz(self):
        orders = ord_rep.load_registred_roz()
        if orders:
            for order in orders:
                self.change_status_item(order.id, 8)



    def test_order(self, order_id):
        orders = ord_rep.load_item_all()
        resp_sour = None
        if not resp_sour:
            tg_cntrl.sendMessage(tg_cntrl.chat_id_info, "Немає такого компоненту ")
        return resp_sour



ord_cntrl = OrderCntrl()




