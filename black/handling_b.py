import os, json, re
from dotenv import load_dotenv
from api.prom import EvoClient
from black.manager_ttn import ManagerTTN

from .telegram_controller import tg_cntrl


env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
TOKEN_PROM = os.getenv("PROM_TOKEN")
prom_cl = EvoClient(TOKEN_PROM)



mg_ttn = ManagerTTN()


# вп: -421982888; розет: -1001822083358; укр: -1001173544690; нп: -1001391714237
chat_id_helper = os.getenv("CHAT_ID_HELPER")
chat_id_np = os.getenv("CH_ID_NP")
chat_id_ukr = "-1001173544690"
chat_id_rozet = "-1001822083358"
chat_id_vp = os.getenv("CHAT_ID_INFO")
invoice_order = None
callback_query_id = None

# def create_status_get(status_order, order_id):
#     dict_status_prom = None
#     print(status_order)
#     if 2 == status_order: # питання
#         dict_status_prom = {
#             "custom_status_id": 142216,
#             "ids": [order_id]
#         }
#     if 1 == status_order: # прийнято
#         dict_status_prom = {
#             "status": "received",
#             "ids": [order_id]
#         }
#     if 3 == status_order: # прийнято
#         dict_status_prom = {
#             "custom_status_id": 137639,
#             "ids": [order_id]
#         }
#     return dict_status_prom

# def send_to_chat(order_id, status, data_in):
#     AUTH_TOKEN = os.getenv("PROM_TOKEN")
#     api_example = EvoClient(AUTH_TOKEN)
#     try:
#         order = api_example.get_order_id(order_id)
#     except:
#         order = None
#         tg_cntrl.sendMessage(chat_id_vp, f"❗️❗️❗️ НЕ ВИЙШЛО отримати замовлення {order_id} від prom спробуйте пізніше")
#         pass
#     print(order)
#     text = data_in["callback_query"]["message"]["text"]
#     # text_for_np = mn_tg_cntrl.send_order_curier(order["order"])
#     # tg_cntrl.sendMessage(chat_id_np, text_for_np)
#     delivery_option = order["order"]["delivery_option"]["id"]
#     print(text)
#     print(delivery_option)
#     if delivery_option == 13013934: # нп
#         tg_cntrl.answerCallbackQuery(callback_query_id, f"Обробляю НП")
#         print(delivery_option)
#         ttn_data = mg_ttn.create_ttn(order["order"])
#         # resp_ok = mg_ttn.add_ttn_crm(order_id, ttn_data)
#         ttn_number = ttn_data["data"][0]["IntDocNumber"]
#         print(f"ttn_number {ttn_number}")
#         data_get_order = text.replace(";ТТН немає", f";{ttn_number}")
#         print(f"data_get_order {data_get_order}")
#         resp = tg_cntrl.sendMessage(tg_cntrl.chat_id_np, data_get_order)
#         print(resp)
#     if delivery_option == 14383961 or delivery_option == 15255183: # розетка мист
#         tg_cntrl.answerCallbackQuery(callback_query_id, f"Відсилаю в Розетку")
#         keyboard_rozet = tg_cntrl.keyboard_generate("Надіслати накладну", order_id)
#         tg_cntrl.sendMessage(tg_cntrl.chat_id_rozet, text, keyboard_rozet)
#         print(status)
#         try:
#             resp_api = api_example.get_set_status(status)
#         except:
#             resp_api = "Статус не змінено"
#             tg_cntrl.sendMessage(tg_cntrl.chat_id_vp, f"Статус не змінено {order_id}")
#         print(resp_api)
#     if delivery_option == 13844336: # укрпошта
#         tg_cntrl.answerCallbackQuery(callback_query_id, f"Відсилаю в Укрпошту")
#         tg_cntrl.sendMessage(tg_cntrl.chat_id_ukr, text)
#         try:
#             resp_api = api_example.get_set_status(status)
#         except:
#             resp_api = "Статус не змінено"
#             tg_cntrl.sendMessage(chat_id_vp, f"Статус не змінено {order_id}")
#         print(resp_api)

def send_request_status(invoice_ttn, invoice_order):
    delivery_type_roz = "rozetka_delivery"
    resp = prom_cl.make_send_ttn(invoice_ttn, invoice_order, delivery_type_roz)
    print("=======")
    print(resp)
    if "error" in resp["status"]:
        error = resp["message"]
        print("Помилка")
        tg_cntrl.answerCallbackQuery(callback_query_id, f"{error}")
        tg_cntrl.sendMessage(chat_id_vp, f"Розетка: {error}")
    else:
        tg_cntrl.answerCallbackQuery(callback_query_id, f"Передано {invoice_order}")
        tg_cntrl.sendMessage(chat_id_vp, f"Что то изменилось: {resp}")

def get_edit_message(data, text):
    chat_id = data["message"]["reply_to_message"]["chat"]["id"]
    message_id = data["message"]["reply_to_message"]["message_id"]
    tg_cntrl.editMessageText(chat_id, message_id, text)
    print(chat_id, message_id, text)

def replace_text_ttn(data, ttn_number):
    text = data["message"]["reply_to_message"]["text"]
    new_text = text.replace(";ТТН немає", f";{ttn_number}")
    return new_text

def search_invoice_ttn(data):
    print("Шукаю розетку ттн")
    invoice_pattern = r'PRM-\d+'
    text = data["message"]["text"]
    search_ttn_pattern = re.findall(invoice_pattern, text)
    if search_ttn_pattern:
        return search_ttn_pattern[0]

def search_order_number(text_message):
    print(f"text_message {text_message}")
    if "Замовлення PROM" in text_message:
        pattern = r'PROM № (\d+)'
        number_order = re.search(pattern, text_message)
        print(number_order)
        return number_order.group(1).strip()

def search_reply_message(data):
    if "reply_to_message" in data["message"] and "text" in data["message"]["reply_to_message"]:
        text_message = data["message"]["reply_to_message"]["text"]
        invoice_order = search_order_number(text_message)
        invoice_ttn = search_invoice_ttn(data)
        if invoice_order and invoice_ttn:
            send_request_status(invoice_ttn, invoice_order)
            text = replace_text_ttn(data, invoice_ttn)
            get_edit_message(data, text)
        else:
            return None

def button_hand(data_in):
    # AUTH_TOKEN = os.getenv("PROM_TOKEN")
    # api_example = EvoClient(AUTH_TOKEN)
    # invoice_pattern = r'PRM-\d+'
    # global callback_query_id
    # callback_query_id = data_in["callback_query"]["id"]
    # data_keyb = json.loads(data_in['callback_query']['data'])
    # text_data_back = data_in["callback_query"]["message"]["reply_markup"]["inline_keyboard"][0][0]["text"]
    search_invoice_ttn(data_in)

    # if "Прийнято" in text_data_back:
    #     status = create_status_get(data_keyb, order_id)
    #     print(status)
    #     print(data_keyb)
    #     if 1 == data_keyb:
    #         responce = send_to_chat(order_id, status, data_in)
    #         print(responce)
    #     if 2 == data_keyb:
    #         tg_cntrl.answerCallbackQuery(callback_query_id, "Питання")
    #         resp_api = api_example.get_set_status(status)
    #         print(resp_api)
    # if "Надіслати накладну" in text_data_back:
    #     tg_cntrl.forceReply(chat_id_vp)
    #     tg_cntrl.answerCallbackQuery(callback_query_id, "Чекаю накладну")
    #     global invoice_order
    #     invoice_order = data_keyb
    return '', 200



