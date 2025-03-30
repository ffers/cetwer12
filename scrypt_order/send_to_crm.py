import os, json, requests, logging, pytz
from dotenv import load_dotenv
from scrypt_order.search_paym import process_order
from black import ord_cntrl 

from utils import OC_logger
from black import tg_cntrl 

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
url_send = os.getenv("URL_TO_CRM")
url_update = os.getenv("URL_TO_UPDATE")


OC_log = OC_logger.oc_log("send_to_crm")


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
                OC_log.info(f"send_to_crm_resp: {resp_crm}")
                if not resp_crm:
                    tg_cntrl.sendMessage(chat_id_helper, f"Сервер не відповідає замовленя не додано {order_id}")
                else:
                    processed_orders.add(order_id)
                    save_processed_orders(processed_orders)
            except:
                resp_crm = None
                tg_cntrl.sendMessage(chat_id_helper, f"❗️❗️❗️ НЕ ВИЙШЛО ДОДАТИ замовлення {order_id} В CRM сторона scrypt")

def send_order_dubl():
    ord_cntrl.load_order_for_code()



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
            return resp
        except:
            print("Сервер не отвечаєт")
            return False