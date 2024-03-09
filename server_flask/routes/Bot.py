from flask import Blueprint, render_template, request
import os
from flask_login import current_user
from dotenv import load_dotenv
from black import TelegramController

tg_cntrl = TelegramController()
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bp = Blueprint('Bot', __name__, template_folder='templates')

@bp.route("/bot", methods=['POST', 'GET'])
def bot():
    if request.method == 'POST':
        data = request.json
        print(request.json)
        try:
            tg_cntrl.await_tg_button(data)
        except:
            print("не вдалося отримати відповідь")
        return {'ok': True}
    return render_template('index.html', user=current_user)

# bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(commands=['button'])
# def button(message):
#     bot.send_message(chat_id, "Hello, did someone call for help?")
#     return 200


# def create_status_get(status_order):
#     if "custom_status_id" in status_order:
#         dict_status_prom = {
#             "custom_status_id": status_order["custom_status_id"],
#             "ids": [status_order["order"]]
#         }
#     if "status" in status_order: # прийнято
#         dict_status_prom = {
#             "status": status_order["status"],
#             "ids": [status_order["order"]]
#         }
#     return dict_status_prom
#
# def send_to_chat(keyboard_json, status, data_in):
#     AUTH_TOKEN = os.getenv("PROM_TOKEN")
#     api_example = EvoClient(AUTH_TOKEN)
#     order_id = keyboard_json["order"]
#     print(order_id)
#     text = data_in["callback_query"]["message"]["text"]
#     delivery_option = send_order(order_id)
#     print(text)
#     print(delivery_option)
#     if delivery_option == 13013934: # нп
#         print(delivery_option)
#         ttn_data = create_ttn_button(order_id)
#         ttn_number = ttn_data["data"][0]["IntDocNumber"]
#         data_get_order = text.replace(";ТТН немає", f";{ttn_number}")
#         print(data_get_order)
#         send_message = send_message_f(chat_id_np, data_get_order)
#     if delivery_option == 14383961 or delivery_option == 15255183: # розетка мист
#         send_message = send_message_f(chat_id_rozet, text)
#         print(status)
#         resp_api = api_example.get_set_status(status)
#         print(resp_api)
#     if delivery_option == 13844336: # укрпошта
#         send_message = send_message_f(chat_id_ukr, text)
#         resp_api = api_example.get_set_status(status)
#         print(resp_api)
#
# def button(data_in):
#     AUTH_TOKEN = os.getenv("PROM_TOKEN")
#     api_example = EvoClient(AUTH_TOKEN)
#     if "callback_query" in data_in:
#         keyboard_json = json.loads(data_in['callback_query']['data'])
#         status = create_status_get(keyboard_json)
#         print(status)
#         if "status" in keyboard_json:
#             responce = send_to_chat(keyboard_json, status, data_in)
#             print(responce)
#             # resp_api = api_example.get_set_status(status)
#             # print(resp_api)
#         if "custom_status_id" in keyboard_json:
#             resp_api = api_example.get_set_status(status)
#             print(resp_api)
