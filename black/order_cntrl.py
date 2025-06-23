import os, logging, sys
from server_flask.db import db
from dotenv import load_dotenv
from datetime import datetime


from .crm_to_telegram import CrmToTelegram
from .np_cntrl import NpCntrl
from .product_analitic_cntrl import ProductAnaliticControl
from .delivery_order_cntrl import DeliveryOrderCntrl
from .prom_cntrl import PromCntrl
from .analitic_cntrl.sour_an_cntrl import SourAnCntrl
from .telegram_cntrl.tg_cash_cntrl import TgCashCntrl
from .product_cntrl import ProductCntrl


from a_service.order_service import OrderServ
from a_service.delivery import NpServ
from a_service import DeliveryOrderServ, StatusProcess
from a_service import tg_serv, TgServ, TextFactory
from a_service import TgServNew, ProductServ
from a_service import EvoService, RozetkaServ, TgServNew, ProductServ
from a_service.order_service import OrderServ, OrderApi
from a_service.order_service.handlers.base import UnpayContext
from a_service.store_service import StoreService


from api import EvoClient, RozetMain, TgClient
from api.nova_poshta.create_data import NpClient


from repository.store_sqlalchemy import StoreRepositorySQLAlchemy
from repository import OrderRep


from utils import my_time
from utils import OC_logger, OSDEBUG

from DTO import OrderDTO




# order1 = StatusProcess.update_order(2487, 6, TelegramController)

#  id |        name        | description
# ----+--------------------+-------------
#   1 | Підтвердити        |
#   2 | Підтвержено        |
#   3 | Оплачено           |
#   4 | Несплачено         |
#   5 | Скасовано          |
#   6 | Предзамовлення     |
#   7 | Питання            |
#   8 | Відправлено        |
#   9 | Отримано           | 
#  10 | Нове               | 
#  11 | Очікує відправленя |
#  12 | Виконано           | 
#  13 | Тест
#  14 | Повернення

sys.path.append('../')

# log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
token_ev = os.getenv("PROM_TOKEN")
token_np = os.getenv("NP_TOKEN")
chat_id_helper = os.getenv("CHAT_ID_HELPER")


crmtotg_cl = CrmToTelegram()



np_cl = NpClient(token_np)
ord_serv = OrderServ()
np_serv = NpServ()
prod_an_cntrl = ProductAnaliticControl()
np_cntrl = NpCntrl()
del_ord_serv = DeliveryOrderServ()
del_ord_cntrl = DeliveryOrderCntrl()



class OrderCntrl: 
    def __init__(self) -> None:
        self.OC_log = OC_logger.oc_log("order_cntrl")
        self.sour = SourAnCntrl()
        self.quan_stok = TgCashCntrl()
        self.tg_cntrl = TgServNew()
        self.np_client = NpClient()
        self.ord_rep = OrderRep()
        self.status_procces = StatusProcess
        self.order_serv = OrderServ()
        self.store_serv = StoreService(repo=StoreRepositorySQLAlchemy(db.session))
        self.prom_cntrl = PromCntrl()
    

        
    def update_history(self, order_id, comment):
        resp = self.order_serv.update_history(order_id, comment)
        return resp
    
    def change_history(self, request_data):
        resp = self.order_serv.change_history(request_data)
        return resp
    
    def reg_17_00(self):
        black_pic = self.tg_cntrl.black_pic()
        dict_order = self.createReg()
        self.OC_log.info(dict_order)
        self.sendTg(dict_order)
        self.OC_log.info("Виконую завдання")
        
    def my_time(self):
        yield (datetime.now())

    def load_all_order(self):
        order = self.ord_rep.load_item_all()
        return order

    def load_confirmed_order(self):
        item = self.ord_rep.load_for_np()
        return item

    def load_registred(self):
        item = self.ord_rep.load_registred()
 
        return item

    def load_registred_roz(self):
        item = self.ord_rep.load_registred_roz()

        return item

    def load_status_id(self, id):
        return self.order_serv.load_status_id(id)
    
    def load_for_order_id(self, order_id):
        return self.ord_rep.load_item(order_id)

    def load_order_for_code(self, order_code):
        order = self.ord_rep.load_for_code(order_code)
        return order.id 

    def load_for_order_code(self, order_code):
        from a_service.order_service.order_serv import OrderServ
        from repository.order_rep import OrderRep
        loader = OrderServ()
        return loader.repo_loader_factory('order_code', order_code, OrderRep(db.session))
        

    # def load_orders_store(self, api_name, token):
    #     return self.order_serv.load_orders_store(api_name,
    #                                             token,
    #                                             OrderCntrl, 
    #                                             TelegramController, 
    #                                             EvoClient,
    #                                             RozetMain)

    def update_client_info(self):
        return self.order_serv.update_client_info()

    def dublicate(self, order_id):
        item = self.ord_rep.load_item(order_id)
        dublicate_item = self.ord_rep.dublicate_item(item)
        ord_prod_old = self.ord_rep.load_prod_order(order_id)
        dublicate_order_prod = self.ord_rep.dublicate_order_prod(dublicate_item, ord_prod_old)
        self.add_order_code(dublicate_item)
        self.send_order_tg(dublicate_item.id)
        return True
    
    def dublicate2(self, order_id):
        pass

    # def add_order(self, order_js):
    #     order_code = order_js["id"]
    #     try:
    #         data_for_tg = crmtotg_cl.manger(order_js)
    #         resp = pr_to_crm_cntr.add_order(order_js, data_for_tg)
    #         print(order_js)
    #         order = self.ord_rep.load_for_code(order_js["id"])
    #         print(f"add_order {order.id}")
    #         bool_1 = del_ord_cntrl.add_item(order.id, 1)
    #         bool_2 = self.examine_address(order_js)
    #         return resp
    #     except:
    #         info = f"Замовленя можливо не додано в CRM {order_code}"
    #         self.OC_log.info(info)
    #         self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_confirm, info)

    # 
    # Для РОЗЕТКІ =======================
    #
    #
    def add_costumer(self, costumer_dto): 
        return self.order_serv.add_costumer(costumer_dto)
    
    def add_recipient(self, recipient_dto):
        return self.order_serv.add_recipient(recipient_dto)

    def add_order2(self, order_obj):
        return self.ord_rep.add_order(order_obj)
    
    def add_order3(self, order_dto):
        return self.order_serv.add_order3(order_dto)
    
    def update_order3(self, order_id, order_dto):
        return self.order_serv.update_order3(order_id, order_dto)
    
    def add_ordered_product(self, product_dto, ord_id):
        prod_cntrl = ProductCntrl()
        prod_db = prod_cntrl.load_by_article(product_dto.article)
        product_dto.order_id = ord_id
        product_dto.product_id = prod_db.id
        product_db = self.ord_rep.add_ordered_product(product_dto)
        return product_db

    #-----==========================
    #
    #
    #

    

    # def examine_address(self, order):
    #     resp_bool = np_serv.examine_address_prom(order)
    #     if not resp_bool:
    #         order_dr = prom_cntrl.get_order(order["id"])
    #         order = order_dr["order"]
    #         order_id = order["id"]
    #         delivery_provider_data = order["delivery_provider_data"]
    #         try:
    #             self.OC_log.info(f"Обробка стандартна, ордер:{order_id}\n Інформація по адресі {delivery_provider_data} ")
    #             self.tg_cntrl.send_message_f(chat_id_helper,
    #                                  f"Обробка стандартна, ордер:{order_id}\n Інформація по адресі {delivery_provider_data} ")
    #             self.update_address(order)
    #         except:
    #             self.tg_cntrl.send_message_f(chat_id_helper,
    #                             f"️❗️❗️❗️ Повторно адреси нема в № {order_id} ")
    #             self.OC_log.info(
    #                 f"Обробка ордера: {order_id}\n "
    #                 f"Інформація по адресі {delivery_provider_data} ")

    def update_address(self, order):
        war_ref = np_serv.examine_address_prom(order)
        # если есть ключ адреса в заказе еще раз додаем адрес,
        # если нет то ето может бить розетка или
        if war_ref:
            if order["delivery_option"]["id"] == 13013934:
                data_address = np_cl.get_s_war_ref(war_ref)
                address_dict_np = np_serv.create_address_dict_np(data_address)
                resp_bool = self.ord_rep.change_address((order["id"]), address_dict_np)
                return resp_bool
            return True
        self.OC_log.info(f"Викликаєм помилку {order}")
        raise

    def add_order_code(self, order):
        while True:
            order_code = ord_serv.generate_order_code()
            item = self.ord_rep.load_for_code(order_code)
            if not item:
                self.ord_rep.add_order_code(order, order_code)
                return

    def send_order_tg(self, order_id, text="🟠 Редагування"):
        order = self.ord_rep.load_item(order_id)
        data_tg_dict = tg_serv.create_text_order(order)
        keyboard_json = self.tg_cntrl.keyboard_func()
        add_text = f"{text}\n{data_tg_dict}"
        resp = self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_confirm, add_text, keyboard_json)
        return True 


    def search_for_phone(self, req):
        search_request = req.args.get('q', '').lower()
        print(search_request) 
        order = self.ord_rep.search_for_all(search_request)
        result = ord_serv.search_for_order(order)
        return result

    def confirmed_order(self, order_id):
        try:
            print("first")
            order = self.ord_rep.load_item(order_id)
            update_analitic = prod_an_cntrl.product_in_order(order)

            delivery = self.check_del_method(order)
            bool_prom = self.definition_source(order, 2)
            if delivery.get("success"):
                crm_status = self.ord_rep.change_status(order_id, 2)
                self.update_history(order_id, "Підтверджено")
                resp_tg = self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_confirm, "{ordered_status} {order_code}".format(**crm_status))
                return True
            return False
        except Exception as e:
            self.OC_log.error(f'confirm_ order: {e}')
            return False

    def result(self, *args):
        result = {
            "crm_status": args[0],
            "bool_prom": args[1],
            "update_analitic": args[2], 
            "delivery": args[3]
        }
        return result

    def question_order(self, order_id):
        order = self.ord_rep.load_item(order_id)
        bool = self.change_status_item(order_id, 5)
        bool_prom = self.definition_source(order, 5)
        return bool

    def double_order(self, order_id):
        order = self.ord_rep.load_item(order_id)
        bool = self.change_status_item(order_id, 15)
        bool_prom = self.definition_source(order, 3)
        return bool
    
    def make_client_store(self, order_code):
        try:
            order_base = self.ord_rep.load_for_order_code(order_code)
            store_data = self.store_serv.get_item(order_base.store_id)
            return EvoClient(store_data.token_market, ProductServ(), store_data)
        except Exception as e:
            self.OC_log.exception(f'{e}')
            if OSDEBUG: print(f'Помилка {e}')

    def definition_source(self, order: OrderDTO, status):
        bool_prom = True
        if order.source_order_id == 2:
            evo_client = self.make_client_store(order.order_code)
            bool_prom = self.prom_cntrl.change_status(order.order_code, status, evo_client)
        print("definition_source:", order.source_order_id)
        print("definition_source:", bool_prom)
        return bool_prom

    def return_order(self, order_id, status):
        order = self.ord_rep.load_item(order_id)
        bool = self.ord_rep.change_status(order_id, status)
        evo_client = self.make_client_store(order.order_code)
        bool_prom = self.prom_cntrl.change_status(order.order_code, 5, evo_client)
        # update_analitic = prod_an_cntrl.product_in_order(order)
        resp_sour_bool = self.sour.return_prod(order)
        # resp = self.check_del_method(order)
        return resp_sour_bool

    def send_storage(self, order_id):
        order = self.ord_rep.load_item(order_id)
        resp_sour = self.sour.confirmed(order)
        return resp_sour

    def check_del_method(self, order):
        resp = False
        text_courier = TextFactory.factory("courier", order)
        if order.delivery_method_id == 1:
            resp = self.del_method_np(order)
        elif order.delivery_method_id == 2 or order.delivery_method_id == 4:
            print("Розетка")
            resp = self.del_method_roz(order, text_courier)
        elif order.delivery_method_id == 3:
            resp = self.del_method_ukr(order, text_courier)
        elif order.delivery_method_id == 5:
            resp = self.del_method_shop(order, text_courier)
        return resp

    def del_method_np(self, order):
        resp = False
        if not order.warehouse_ref:
            raise ValueError('Треба оновити адресу')
        np_resp = np_cntrl.manager_data(order)  # обработка зкаказа из срм создание ттн, телеграм курьеру заказ, додавання в пром ттн
        if np_resp["success"] == True:
            doc_ttn = np_resp["data"][0]["IntDocNumber"]
            resp_ttn = self.add_ttn_crm(order.id, doc_ttn)
            order = self.ord_rep.load_item(order.id)
            text_courier = TextFactory.factory("courier", order)
            self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_np, text_courier)
            del_ord_cntrl.update_item(np_resp, order.id)
            if order.source_order_id == 2:
                self.send_ttn_to_market(order)
        elif 'OptionsSeat is empty' in np_resp["errors"]:
            resp = np_resp
            self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_confirm,
                                 "❗️❗️❗️ ТТН не створено - не вказано обʼєм")
        else:
            resp = np_resp
            self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_confirm,
                                 f"❗️❗️❗️ ТТН не створено - {resp}")
        return np_resp
    
    def send_ttn_to_market(self, order):
        evo_client = self.make_client_store(order.order_code)
        resp_prom_ttn = self.prom_cntrl.send_ttn(order.order_code, order.ttn, "nova_poshta", evo_client)
        self.OC_log.info(f'del_method_np {resp_prom_ttn}')
        if OSDEBUG: print(f'del_method_np {resp_prom_ttn}')
        if resp_prom_ttn != {'status': 'success'}:
            self.self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_confirm,
                            f"❗️❗️❗️ Проблема підвязкі ттн замовлення: {order.order_code} - сповістити адміна")
        else:
            self.OC_log.info(f'ТТН підвязано {order.order_code}')
            if OSDEBUG: print(f'ТТН підвязано {order.order_code}')
    def add_ttn_crm(self, order_id, ttn):
        resp = self.ord_rep.add_ttn_crm(order_id, ttn)
        return resp

    def del_method_roz(self, order, text_courier): 
        keyboard_rozet = self.tg_cntrl.keyboard_generate("Надіслати накладну", order.order_code)
        resp = self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_rozet, text_courier, keyboard_rozet)
        return {"success": True}

    def del_method_ukr(self, order , text_courier):
        resp = self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_ukr, text_courier)
        return {"success": True}

    def del_method_shop(self, order, text_courier):
        resp = self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_shop, text_courier)
        return {"success": True}

    def delete_order(self, id):
        print(f"delete order {id}")
        bool = self.ord_rep.delete_order(id)
        return bool

    def change_status(self, data):
        orders, status = ord_serv.parse_dict_status(data)
        print("WTF")
        for order in orders:
            print (f"%s %s try change" % (order, status))
            self.change_status_item(order, status)
        # bool = self.ord_rep.change_status_list(orders, status)
        return True

    def change_status_item(self, id, status):
        resp = self.ord_rep.change_status(id, status)
        StatusProcess.factory(id, int(status), TgServ, OrderRep)
        return resp   # resp.update( {"message_id": resp_tg["result"]["message_id"]})
 
    def change_status_roz(self):
        orders = self.ord_rep.load_registred_roz()
        if orders:
            for order in orders:
                self.change_status_item(order.id, 8)


 
    def test_order(self, order_id):
        orders = self.ord_rep.load_item_all()
        resp_sour = None
        if not resp_sour:
            self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_info, "Немає такого компоненту ")
        return resp_sour
    
    def order_api_factory(self, get_type):
        pass

    async def get_status_unpay(self, store_crm_token, marketplace_token):   
        store_data = StoreRepositorySQLAlchemy(db.session).get_token(store_crm_token)
        tg_token = os.getenv('TELEGRAM_BOT_TOKEN')
        evo_serv = EvoService(EvoClient(marketplace_token, ProductServ(), store_data))
        roz_serv = RozetkaServ(RozetMain(marketplace_token, ProductServ(), store_data))
        tg_serv = TgServNew(TgClient(tg_token))
        order_repo = OrderRep(db.session)
        store_repo = StoreRepositorySQLAlchemy(db.session)
        store_proc = OrderApi
        order_serv = OrderServ(
            evo_serv=evo_serv, 
            roz_serv=roz_serv,
            tg_serv=tg_serv,
            order_repo=order_repo,
            store_repo=store_repo, 
            )
        ctx = UnpayContext(
                        evo_serv,
                        roz_serv,
                        tg_serv,
                        order_repo,
                        store_repo,
                        OC_logger.oc_log('unpay_test'),
                        store_proc,

            )
        ctx.state.token = store_crm_token
        result = order_serv.get_status_unpay_v3(ctx) 
    




ord_cntrl = OrderCntrl()




