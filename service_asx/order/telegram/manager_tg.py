from telegram import TgClient
from dotenv import load_dotenv
import os, logging
from server_flask.models import Orders
# from order_bot import button_hand

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)

tg_cl = TgClient()

chat_id_np = os.getenv("CH_ID_NP") #"-1001391714237" -421982888

class ManagerTg():
    def __init__(self):
        logging.basicConfig(filename='../common_asx/log_order.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def send_order_curier(self, order):
        order_id = order["id"]
        logging.info(f"Обробка ордера send_curier: {order_id}")
        client_name = order["client_last_name"] + " " + order["client_first_name"]
        delivery_option = order["delivery_option"]["name"]
        delivery_address = order["delivery_address"]
        payment_option = order["payment_option"]["name"]
        full_price = order["full_price"]
        if "client_notes" in order and order["client_notes"]:
            client_notes = "Нотатка: " + order["client_notes"]
        else:
            client_notes = "Нотаток від клієнта нема"
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
            formatted_text += f"{product['artikul']} - {product['quantity']} {product['measure_unit']} - {product['price']} \n"
            formatted_text += f"Название: {product['name_multilang']}"

        data_get_order = (
            f"🍎 {up_text} Cумма {sum_order}\n\n{client_notes}\n\n"
            f"{delivery_address}\n\n🍎 Замовлення №{order_id}\n\n{phone_num};ТТН немає\n{client_name}\n{delivery_option}\n"
            f"Способ оплати - {payment_option}, {status} \n\n  На будь якій випадок:\n"
            f"{formatted_text}\n\n=========================================================="
        )


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

    def send(self, order):
        order_product = order.ordered_product
        if order.description:
            description = "🍏 Нотатка:\n" + order.description
        else:
            description = "Нотаток від клієнта нема"
        payment_method = order.payment_method
        if order.sum_before_goods:
            sum_check = order.sum_before_goods
        else:
            sum_check = order.sum_price
        product_article = ""
        product_text = "На всяк випадок:\n"
        for product in order_product:
            product_article += f"🍏 {product.products.article} - {product.quantity}шт - {product.price}\n"
            product_text += f" {product.products.product_name}\n"
        data_get_order = (
            f"{product_article} Сумма: {order.sum_price} \n\n{description}\n\n"
            f"{order.city_name}, {order.warehouse_text} \n\n🍏 Замовлення {order.source_order.name} №{order.id}\n"
            f"\n{order.phone};{order.ttn}\n{order.client_lastname} {order.client_firstname}\n"
            f"Способ оплати - {payment_method.name}, {sum_check} \n\n"
            
            f"{product_text}\n=========================================================="
        )
        tg_cl.send_message_f(chat_id_np, data_get_order)

    def see_flag(self, order, flag=None):
        print(f"see_flag {flag}")
        if flag == "Надіслати накладну":
            self.send_order_curier(order)
        if flag == "crm_to_telegram":
            self.send(order)


    # def await_tg_button(self, data):
    #     resp = button_hand(data)
    #     return resp
