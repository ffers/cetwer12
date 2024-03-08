import os, json, requests, logging, pytz, sys
from os.path import join, dirname
from dotenv import load_dotenv
from .keyboard_tg import TgKeyboard
from .current_changes_order import Changes

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
ch_cl = Changes()
tg_keyboard = TgKeyboard()
logging.basicConfig(filename='../common_asx/log_order.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
file_get_ord = "../common_asx/get_orders.json"
georgia_timezone = pytz.timezone('Asia/Tbilisi')
data_sms = {
    "phone" : ["380989323122"],
    "message" : "test text",
    "src_addr" : "Jemis"
        }
data_status = {
    "id_sms": ["1092704994"],
    "custom_status_id": 0
}
# -421982888 -511339281  -1001979021180 chat pidtverzgenya
chat_id_pid = os.getenv("CHAT_ID_CONFIRMATION")
# Завантаження оброблених ордерів із файлу
logging.info("Шукаєм нові замовленя...")

dict_status_prom = {
        "status": "received",
        "ids": [ 259039935 ]
        }

def load_processed_orders():
    try:
        with open(file_get_ord, "r") as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

# Збереження оброблених ордерів у файл
def save_processed_orders(processed_orders):
    with open(file_get_ord, "w") as file:
        json.dump(list(processed_orders), file)

# Приклад обробки ордерів
def send_order():
    processed_orders = load_processed_orders()
    with open("common/data.json", "r", encoding='utf-8') as file:
        data = json.load(file)
    for order in data["orders"]:
        order_id = order["id"]
        if order_id not in processed_orders:
            delivery_name = order["delivery_option"]
            if delivery_name != None:
                logging.info(f"Обробка ордера: {order_id}")
                client_name = order["client_last_name"] + " " +order["client_first_name"]
                delivery_option = order["delivery_option"]["name"]
                delivery_address = order["delivery_address"]
                payment_option = order["payment_option"]["name"]
                full_price = order["full_price"]
                if "client_notes" in order and order["client_notes"]:
                    client_notes = "🍎 Нотатка: " + order["client_notes"]
                else:
                    client_notes = "Нотаток від клієнта нема"
                status = ""
                if order["payment_option"]["id"] == 7547964:
                    status = payment_data_status(order["payment_data"])
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
                                  f"{delivery_address}\n\n🍎 Замовлення № {order_id}\n\n{phone_num};ТТН немає\n{client_name}\n{delivery_option}\n"
                                  f"Способ оплати - {payment_option}, {status} \n\n  На будь якій випадок:\n"
                                  f"{formatted_text}\n\n=========================================================="
                )
                delivery_option = order["delivery_option"]["id"]
                keyboard_json = tg_keyboard.keyboard_func(order_id, delivery_option)
                print(keyboard_json)
                size_j = sys.getsizeof(keyboard_json)
                responce = send_message(chat_id_pid, data_get_order, keyboard_json)
                print(size_j)

                # Додавання ордера до множини оброблених ордерів
                processed_orders.add(order_id)
                save_processed_orders(processed_orders)

def get_from_env(key):
    dotenv_path = join(dirname(__file__), 'documents/.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)

def send_message(chat_id, text, keyboard_json=None):
    method = "sendMessage"
    token = get_from_env("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/{method}"
    if keyboard_json:
        data = {"chat_id": chat_id, "text": text, 'parse_mode': 'Markdown', "reply_markup":keyboard_json}
    else:
        data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def payment_data_status(payment_data):
    print(payment_data)
    if payment_data != None:
        if "unpaid" in payment_data["status"]:
            status_pay = "Несплачено"
            ch_cl.search_pay()
        else:
            status_pay = "Замовлення сплачено"
        print(status_pay)
        return status_pay
    else:
        payment_data = "Несплачено"
        ch_cl.search_pay()
    return payment_data

