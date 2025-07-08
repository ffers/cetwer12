import os, json, re

from server_flask.db import db

from utils import OC_logger

from dotenv import load_dotenv

from api.prom import EvoClient

from a_service import TgServNew, ProductServ

from repository.store_sqlalchemy import StoreRepositorySQLAlchemy


tg_cntrl = TgServNew()
chat_id_helper = os.getenv("CHAT_ID_HELPER")
chat_id_np = os.getenv("CH_ID_NP")
chat_id_ukr = "-1001173544690"
chat_id_rozet = "-1001822083358"
chat_id_vp = os.getenv("CHAT_ID_INFO")
invoice_order = None
callback_query_id = None

class HandlerB:
    def __init__(self, order_cntrl=None):
        self.log = OC_logger.oc_log('handling_b')
        self.ord_cntrl = order_cntrl

    def load_store(self):
        try:
            api_name = 'jemis'
            self.store_data = StoreRepositorySQLAlchemy(db.session).get_token(api_name)
            return EvoClient(
                os.getenv("PROM_TOKEN"),
                ProductServ(),
                self.store_data,
                )
        except Exception as e:
            self.log.exception(f'{e}')

# вп: -421982888; розет: -1001822083358; укр: -1001173544690; нп: -1001391714237

    def send_request_status(self, invoice_ttn, order_id):
        delivery_type_roz = "rozetka_delivery"
        order_id = re.sub(r"\D", "", order_id)
        prom_cl = self.load_store()
        resp = prom_cl.send_ttn(order_id, invoice_ttn, delivery_type_roz)
        print("=======")
        print(resp)
        if "status" in resp:
            if "error" in resp["status"]:
                error = resp["message"]
                print("Помилка")  
                tg_cntrl.sendMessage(chat_id_rozet, f"Помилка: {error} {order_id}")
            else:
                tg_cntrl.sendMessage(chat_id_rozet, "Підвязано ✅")
                return True
        else: 
            tg_cntrl.sendMessage(chat_id_rozet, f"Помилка {resp} {invoice_order}")

    def get_edit_message(self, data, text):
        chat_id = data["message"]["reply_to_message"]["chat"]["id"]
        message_id = data["message"]["reply_to_message"]["message_id"]
        tg_cntrl.editMessageText(chat_id, message_id, text)
        print(chat_id, message_id, text)

    def replace_text_ttn(self, text, ttn_number):
        new_text = text.replace(";ТТН немає", f";{ttn_number}")
        return new_text

    '''
    поперше треба додати в обробку додавати інші группи
    по друге трееба шукати цифри по кількості
    доодати перевірку на вихідний store
    '''

    def search_invoice_ttn(self, data):
        print("Шукаю розетку ттн")
        invoice_pattern = r'(PRM-\d+|RMP-\d+)'
        if data["message"]:
            if "text" in data["message"]:
                text = data["message"]["text"]
                search_ttn_pattern = re.findall(invoice_pattern, text)
                if search_ttn_pattern:
                    return search_ttn_pattern[0]
        return None

    def search_order_number(self, text_message): # якщо це чат розетки,
        print(f"text_message {text_message}")
        if "Замовлення" in text_message:
            pattern = r'Замовлення № (\S+)'
            number_order = re.search(pattern, text_message)
            print(f"wait {number_order}")
            return number_order.group(1).strip()

    def update_order(self, invoice_ttn, invoice_order):
        order = self.ord_cntrl.load_for_order_code(invoice_order)
        if order:
            order_id = order.id
            resp_ttn = self.ord_cntrl.add_ttn_crm(order_id, invoice_ttn)
            resp_status = self.ord_cntrl.change_status_item(order_id, 11)
            return True, None
        else:
            print("Нема такого замовлення")
            return False, "Нема такого замовлення"

    def update_text_tg(self, data, text_message, invoice_ttn):
        text = self.replace_text_ttn(text_message, invoice_ttn)
        self.get_edit_message(data, text)
        return True

    def search_reply_message(self, data): #працює з усіма відповідями не бачу фільтраціїї чату
            text_message = data["message"]["reply_to_message"]["text"]
            invoice_order = self.search_order_number(text_message)
            invoice_ttn = self.search_invoice_ttn(data)
            if invoice_order and invoice_ttn:
                resp_update = self.update_order(invoice_ttn, invoice_order)
                resp_tg = self.update_text_tg(data, text_message, invoice_ttn)
                resp_prom = self.send_request_status(invoice_ttn, invoice_order)
            else:
                return None





