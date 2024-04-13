import os
from dotenv import load_dotenv
from api import tg_api

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
chat_id_helper = os.getenv("CHAT_ID_HELPER") # вп: -421982888; розет: -1001822083358; укр: -1001173544690; нп: -1001391714237
chat_id_np = os.getenv("CH_ID_NP")
chat_id_ukr = os.getenv("CH_ID_UKR")
chat_id_rozet = os.getenv("CH_ID_ROZ")
chat_id_vp = os.getenv("CHAT_ID_INFO")
ch_id_sk = os.getenv("CH_ID_SK")

class TelegramController():
    def __init__(self):
        self.chat_id_info = os.getenv("CHAT_ID_HELPER")
        self.chat_id_np = os.getenv("CH_ID_NP")
        self.chat_id_ukr = os.getenv("CH_ID_UKR")
        self.chat_id_rozet = os.getenv("CH_ID_ROZ")
        self.chat_id_vp = os.getenv("CHAT_ID_INFO")
        self.chat_id_sk = os.getenv("CH_ID_SK")


    def sendPhoto(self):
        chat_list = [self.chat_id_ukr, self.chat_id_rozet, self.chat_id_np]
        for chat in chat_list:
            resp = tg_api.sendPhoto(chat, 'AgACAgIAAxkBAAIMl2YWFuaONHD9_7SWvzDiiK8vmNQSAAK31jEbGsoISBKbThvzHGUpAQADAgADbQADNAQ')
            print(resp)

    def sendMessage(self, chat_id, text, keyboard_json=None):
        resp = tg_api.send_message_f(chat_id, text, keyboard_json)
        return resp

    def answerCallbackQuery(self, callback_query_id, text):
        resp = tg_api.answerCallbackQuery(callback_query_id, text)
        return resp

    def forceReply(self, chat_id, callback_query_id=None, text=None):
        resp = tg_api.forceReply(chat_id, callback_query_id, text)
        return resp

    def editMessageText(self, chat_id, message_id, text):
        resp = tg_api.editMessageText(chat_id, message_id, text)
        return resp

    def keyboard_generate(self, order_id, delivery_option):
        resp = tg_api.keyboard_func(order_id, delivery_option)
        return resp

tg_cntrl = TelegramController()

