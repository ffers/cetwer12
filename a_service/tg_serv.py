
from dotenv import load_dotenv
import os, logging, re
import html
from datetime import datetime
from .telegram_handler.text_formater.text_order_courier import TextOrderCourier

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)

class TgServ():
    def __init__(self):
        logging.basicConfig(filename='../common_asx/log_order.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



    def payment_data_status(self, payment_data):
        print(payment_data)
        if payment_data != None:
            if "unpaid" in payment_data["status"]:
                status_pay = "Несплачено"
            else:
                status_pay = "Замовлення сплачено"
            print(status_pay)
            return status_pay
        else:
            payment_data = "Несплачено"
        return payment_data

    def create_text_order(self, order):
        ttn = order.ttn if order.ttn else "ТТН немає"
        if order.description:
            description = "🟢 Нотатка:\n" + order.description
        else:
            description = "Нотаток від клієнта нема"
        if order.sum_before_goods:
            sum_check = order.sum_before_goods
        else:
            sum_check = order.sum_price 
        product_article = ""
        event_date = order.timestamp.strftime("%d-%m-%Y %H:%M")
        product_text = "На всяк випадок:\n"
        for product in order.ordered_product:
            product_article += f"🟢 {product.products.article} - {product.quantity}шт - {product.price}\n"
            product_text += f" {product.products.product_name}\n"
        data_get_order = (
            f"{product_article} Сумма: {order.sum_price} \n\n{description}\n\n"
            f"{order.city_name}, {order.warehouse_text} \n\n🟢 {order.source_order.name} Замовлення № {order.order_code}\n"
            f"{event_date}\n"
            f"{order.history}\n"
            f"Cтатус: {order.ordered_status.name}\n"
            f"\n{order.phone};{ttn}\n{order.client_lastname} {order.client_firstname}\n"
            f"Спосіб доставки - {order.delivery_method.name}\n"
            f"Спосіб оплати - {order.payment_method.name}, {sum_check} \n\n"
            f"{product_text}\n=========================================================="
        )
        return data_get_order
    


    def check_ttn(self, order):
        ttn = "ТТН немає"
        if order.ttn:
            ttn = order.ttn
        return ttn

    def see_flag(self, order, flag=None):
        print(f"see_flag {flag}")
        if flag == "Надіслати накладну":
            self.send_order_curier(order)
        if flag == "crm_to_telegram":
            self.send(order)

    def search_order_number(self, text_message):
        print(f"text_message {text_message}")
        if "Замовлення №" in text_message:
            pattern = r'Замовлення № (\S+)'
            number_order = re.search(pattern, text_message)
            print(number_order)
            return number_order.group(1).strip()

    def await_button_parse(self, data):
        text_order = data["callback_query"]["message"]["text"]
        data_keyb = data['callback_query']['data']
        text_data_back = data["callback_query"]["message"]["reply_markup"]\
            ["inline_keyboard"][0][0]["text"]
        return text_order, data_keyb, text_data_back

    def replace_text_ttn(self, data, ttn_number):
        text = data["message"]["reply_to_message"]["text"]
        new_text = text.replace(";ТТН немає", f";{ttn_number}")
        return new_text


    # def await_tg_button(self, data):
    #     resp = button_hand(data)
    #     return resp

tg_serv = TgServ()

class TextFactory:
    @staticmethod
    def factory(cmd, order):
        commands = {
            "courier": TextOrderCourier,
        } 
        if cmd in commands:
            return commands[cmd](order).builder(order)
        return f"Немає Текста для {cmd}"