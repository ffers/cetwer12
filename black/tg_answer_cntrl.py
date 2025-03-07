import os
from dotenv import load_dotenv
from .manager_ttn import ManagerTTN
from a_service.tg_serv import tg_serv
from a_service import BotProductSrv
from black.crm_to_telegram import CrmToTelegram
from .add_order_to_crm import PromToCrm
from .handling_b import search_reply_message
from a_service.update_to_crm import up_to_srm
from .telegram_controller import tg_cntrl, TelegramController
from .order_cntrl import ord_cntrl, OrderCntrl
from .analitic_cntrl.sour_an_cntrl import SourAnCntrl
from a_service import TgAnswerSerw, ResponceDirector
from .telegram_cntrl.tg_cash_cntrl import TgCashCntrl


env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
ch_id_sk = os.getenv("CH_ID_SK")

class TgAnswerCntrl:
    def __init__(self):
        self.arrival = TgCashCntrl()
        self.serv = TgAnswerSerw()
        self.order_cntrl = OrderCntrl()
        self.bot_color = BotProductSrv()
        self.send_order = CrmToTelegram()
        self.add_order = PromToCrm()
        self.manager_ttn = ManagerTTN()

    def await_order(self, order, flag=None, id=None):
        print(f"ДИвимось флаг {flag}")
        resp = None
        if flag == "prom_to_crm":
            data_for_tg = self.send_order.manger(order)
            resp = self.add_order.add_order(order, data_for_tg)
        if flag == "update_to_crm":
            resp = up_to_srm.manager(order)
        else:
            tg_serv.see_flag(order, flag)
        return resp

    def await_interface(self, order_id):
        ttn_data = self.manager_ttn.create_ttn(order_id)
        resp_ok = self.manager_ttn.add_ttn_crm(order_id, ttn_data)
        return ttn_data

    def await_cabinet_json(self, data):
        if "search_city" in data["name"]:
            pass

    def await_order_cab_tg(self, order, flag=None, id=None): # дубль фукціі await_order щоб обійти діспетчер
        print(f"see_flag {flag}")
        resp = None
        if flag == "Надіслати накладну":
            resp = tg_serv.send_order_curier(order)
        if flag == "crm_to_telegram":
            resp = tg_serv.send(order)
        return resp

    def await_tg_button(self, data):
        result = ResponceDirector().construct(data, OrderCntrl, SourAnCntrl, TelegramController)
        print(result, "tg_command_new")
        if "message" in data: #працює з усіма відповдями
            self.await_telegram(data)
            # button_hand(data)
        if "callback_query" in data:
            self.await_button(data)
        return result

    def await_telegram(self, data): #працює з чатами Склад, Каштан, Розетка
        chat_id = data["message"]["chat"]["id"]
        
        # return 200, "Ok"
        if int(ch_id_sk) == chat_id:
            print("Отримали повідомлення з Робочого чату")
            text_colour = self.bot_color.work_with_product(data)
            tg_cntrl.sendMessage(tg_cntrl.chat_id_sk, text_colour)
        if int(tg_cntrl.chat_id_cash) == chat_id:
            print("Hello")
            self.arrival.sort(data)
        if int(tg_cntrl.chat_id_rozet) == chat_id:
            if ("reply_to_message" in data["message"] and
                    "text" in data["message"]["reply_to_message"]):
                search_reply_message(data)
                return 200, "ok"


    def await_button(self, data): #працює з Підтвердженнями
        chat_id = data["callback_query"]["message"]["chat"]["id"]
        if int(tg_cntrl.chat_id_confirm) == chat_id:
            key = data["callback_query"]["message"]["reply_markup"]
            call_back_id = data["callback_query"]["id"]
            tg_cntrl.answerCallbackQuery(call_back_id, "Працюю")
            # resp_tg = tg_cntrl.sendMessage(tg_cntrl.chat_id_confirm, "Працюю")
            # send_message_id, send_chat_id = self.serv.id_message(resp_tg)
            if "inline_keyboard" in key:
                text_order, data_keyb, text_data_back = tg_serv.await_button_parse(data)
                print(f"need {key}")
                order_id = tg_serv.search_order_number(text_order)
                order_obj = ord_cntrl.load_for_order_code(order_id)
                resp = self.defintion_status(data_keyb, order_obj.id)
                # tg_cntrl.deleteMessage(tg_cntrl.chat_id_confirm, send_message_id)
                return resp

    def defintion_status(self, data_keyb, order_id):
        resp = None
        print(f"data_keyb {data_keyb}")
        if "1" == data_keyb:
            resp = ord_cntrl.confirmed_order(order_id)
            print(resp) 
        if "2" == data_keyb:
            resp = ord_cntrl.question_order(order_id)
        return resp



tg_answ_cntrl = TgAnswerCntrl()





