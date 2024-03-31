from telegram import TgClient
from helperkit import FileKit
from dotenv import load_dotenv
import os, json, requests

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
fl_cl = FileKit()
tg_cl = TgClient()
elements_to_remove = set()


examine_address_file = "../common_asx/examine_address.json"
data_order = "../common_asx/data.json"
url_update = 'http://localhost:5000/cabinet/orders/get_product/update_with_prom'

  #-421982888 /// -1001979021180 chat pidtverzgenya /// CHAT_ID_CONFIRMATION //// CHAT_ID_INFO
chat_id = os.getenv("CHAT_ID_HELPER")

class ExamineAddress:
    def search_canceled(self):
        data = fl_cl.load_file_json(examine_address_file)
        save_order = set(data)
        print("Дивимось чи скасовано замовленя")
        data_all_order = fl_cl.load_file_json(data_order)
        for order in data_all_order["orders"]:
            delivery_provider_data = order["delivery_provider_data"]["recipient_warehouse_id"]
            if order["delivery_provider_data"]:
                if not order["delivery_provider_data"]["recipient_warehouse_id"]:
                    if order["id"] not in save_order:
                        print("замовленя без адреси знайдені")
                        order_id = order["id"]
                        save_order.add(order_id)
                        order_list = list(save_order)
                        fl_cl.save_file_json(examine_address_file, order_list)
                        tg_cl.send_message_f(chat_id, f"Скасовано {order_id}")
                        try:
                            self.send_http_json(order_id, "canceled")  # відправляєм в базу данних
                        except:
                            tg_cl.send_message_f(chat_id, f"не вийшло додати в crm: Скасовано {order_id}")
