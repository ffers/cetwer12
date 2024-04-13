import os
from dotenv import load_dotenv
from .manager_ttn import ManagerTTN
from a_service.manager_tg import mn_tg_cntrl
from a_service import BotProductSrv
from a_service.order import OrderServ
from black.crm_to_telegram import CrmToTelegram
from repository import OrderRep
from .product_analitic_cntrl import ProductAnaliticControl
from .add_order_to_crm import PromToCrm
from .handling_b import search_reply_message, button_hand
from a_service.update_to_crm import up_to_srm

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
ch_id_sk = os.getenv("CH_ID_SK")

pr_bt_srv = BotProductSrv()
ord_serv = OrderServ()
ord_rep = OrderRep()
crmtotg_cl = CrmToTelegram()
crm_cl = PromToCrm()
mng_cl = ManagerTTN()
prod_an_cntrl = ProductAnaliticControl()

class TgAnswerCntrl:
    def await_order(self, order, flag=None, id=None):
        print(f"ДИвимось флаг {flag}")
        resp = None
        if flag == "prom_to_crm":
            data_for_tg = crmtotg_cl.manger(order)
            resp = crm_cl.add_order(order, data_for_tg)
        if flag == "update_to_crm":
            resp = up_to_srm.manager(order)
        else:
            mn_tg_cntrl.see_flag(order, flag)
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
            resp = mn_tg_cntrl.send_order_curier(order)
        if flag == "crm_to_telegram":
            resp = mn_tg_cntrl.send(order)
        return resp

    def await_tg_button(self, data):
        if "message" in data:
            search_reply_message(data)
            self.await_telegram(data)
        if "callback_query" in data:
            button_hand(data)
        return '', 200

    def await_telegram(self, data):
        if "text" in data["message"]:
            print("Отримав повідомленя в тексті")
            if "entities" in data["message"]:
                command = data["message"]["entities"][0]["type"]
                if "bot_command" in command:
                    print("Отримав команду боту")
        chat_id = data["message"]["chat"]["id"]
        print(chat_id)
        print(ch_id_sk)
        if int(ch_id_sk) == chat_id:
            print("Отримали повідомлення з Робочого чату")
            pr_bt_srv.work_with_product(data)


tg_answ_cntrl = TgAnswerCntrl()





