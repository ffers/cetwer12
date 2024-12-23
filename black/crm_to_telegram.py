import logging, os, sys, json
from dotenv import load_dotenv
from .telegram_controller import tg_cntrl
import html


env_path = '../common_asx/.env'

load_dotenv(dotenv_path=env_path)


class CrmToTelegram:
    def __init__(self):
        self.chat_id_pid = os.getenv("CHAT_ID_CONFIRMATION")
    def manger(self, order):
        try:
            data_for_tg = self.create(order)
            return data_for_tg
        except:
            tg_cntrl.sendMessage(tg_cntrl.chat_id_info, "Помилка надсиланя замовленя в тг")

    def create(self, order):
        order_id = order["id"] 
        delivery_name = order["delivery_option"]
        if delivery_name != None:
            logging.info(f"Обробка ордера: {order_id}")
            client_name = order["client_last_name"] + " " + order["client_first_name"]
            delivery_option = order["delivery_option"]["name"]
            delivery_address = order["delivery_address"]
            payment_option = order["payment_option"]["name"]
            if "client_notes" in order and order["client_notes"]:
                client_notes = "🍎 Нотатка: " + order["client_notes"]
            else:
                client_notes = "Нотаток від клієнта нема"
            status = ""
            if order["payment_option"]["id"] == 7547964:
                status = self.payment_data_status(order["payment_data"])
            all_products = []
            for sku in order["products"]:
                product = { 
                    "artikul": sku["sku"],
                    "name_multilang": sku["name_multilang"]["uk"],
                    "price": sku["price"],
                    "quantity": sku["quantity"],
                    "measure_unit": sku["measure_unit"],
                    "image_url": sku["image"],
                    "total_price": sku["total_price"]
                }
                all_products.append(product)

            phone_num = order["phone"]
            sum_order = order["full_price"]
            formatted_text = ""
            up_text = ""
            for product in all_products:
                up_text += f"{product['artikul']} - {product['quantity']} {product['measure_unit']} - {product['price']} \n"
                formatted_text += f"{product['artikul']} - {product['name_multilang']}\n"

            data_get_order = (
                f"🍎 {up_text} Cумма {sum_order}\n\n{client_notes}\n\n"
                f"{delivery_address}\n\n🍎 Замовлення № {order_id}\n\n{phone_num};ТТН немає\n{client_name}\n{delivery_option}\n"
                f"Способ оплати - {payment_option}, {status} \n\n  На будь якій випадок:\n"
                f"{formatted_text}\n\n=========================================================="
            )
            delivery_option = order["delivery_option"]["id"]
            keyboard_json = tg_cntrl.keyboard_func()
            size_j = sys.getsizeof(keyboard_json)
            resp_tg = tg_cntrl.sendMessage(self.chat_id_pid, data_get_order, keyboard_json)
            print(resp_tg)
            data_for_tg = self.bd_tg(resp_tg)
            print(f"data_for_tg {data_for_tg}")
            return data_for_tg

    def payment_data_status(self, payment_data):
        print(payment_data)
        status_pay = "Несплачено"
        if payment_data:
            status = payment_data.get("status")
            if status == "paid":
                status_pay = "Замовлення сплачено"
            elif status == "refunded":
                status_pay = "Повернуто!"
            else:
                status_pay = "Несплачено"
        return status_pay

    def bd_tg(self, resp_tg):
        if resp_tg:
            data = {
                "message_id": resp_tg["result"]["message_id"],
                "chat_id": resp_tg["result"]["chat"]["id"],
                "text": resp_tg["result"]["text"]
            }
            print(data)
            return data
