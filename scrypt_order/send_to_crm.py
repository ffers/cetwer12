import os, json, requests, logging, pytz, sys
from os.path import join, dirname
from dotenv import load_dotenv
from .current_changes_order import Changes
from scrypt_order.search_paym import process_order
from telegram import TgClient

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
url_send = os.getenv("URL_TO_CRM")
url_update = os.getenv("URL_TO_UPDATE")


ch_cl = Changes()
tg_cl = TgClient()
logging.basicConfig(filename='../common_asx/log_order.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
file_get_ord = "../common_asx/get_orders.json"
file_load = "../common_asx/data.json"
georgia_timezone = pytz.timezone('Asia/Tbilisi')

# -421982888 -511339281  -1001979021180 chat pidtverzgenya
chat_id_pid = os.getenv("CHAT_ID_CONFIRMATION")
chat_id_info = os.getenv("CHAT_ID_INFO")
chat_id_helper = os.getenv("CHAT_ID_HELPER")
# Завантаження оброблених ордерів із файлу
logging.info("Шукаєм нові замовленя...")


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

def load_file(file_load):
    with open(file_load, "r", encoding='utf-8') as file:
        data = json.load(file)
    return data

# Приклад обробки ордерів
def send_order():
    processed_orders = load_processed_orders()
    data = load_file(file_load)
    process_order()
    for order in reversed(data["orders"]):
        order_id = order["id"]
        if order_id not in processed_orders:
            try:
                resp_crm = send_http_json(order, "create_order")
            except:
                resp_crm = None
                tg_cl.send_message_f(chat_id_helper, f"❗️❗️❗️ НЕ ВИЙШЛО ДОДАТИ замовлення {order_id} В CRM сторона scrypt")
            processed_orders.add(order_id)
            save_processed_orders(processed_orders)


def send_http_json(data, flag):
    token = os.getenv("SEND_TO_CRM_TOKEN")
    json_data = json.dumps(data)
    url = None
    if flag == "create_order":
        url = url_send
    elif flag == "update_order":
        url = url_update
    if url:
        resp = None
        headers = {'Content-Type': 'application/json', "Authorization": token}
        try:
            resp_json = requests.post(url, data=json_data, headers=headers, timeout=5)
            resp = json.loads(resp_json.content)
            print(resp)
        except:
            print("Сервер не отвечаєт")
        return resp