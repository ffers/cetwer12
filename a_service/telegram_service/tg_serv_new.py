

from utils  import wrapper
from utils import OC_logger
from api import TgClient
import os


class TgServNew:
    def __init__(self, tg_cl=None):
        self.client = TgClient()
        self.env = os.getenv("ENV")
        self.logger = OC_logger.oc_log("telegram_serv_new")
        self.chat_id_info = os.getenv("CHAT_ID_HELPER")
        self.chat_id_np = os.getenv("CH_ID_NP")
        self.chat_id_ukr = os.getenv("CH_ID_UKR")
        self.chat_id_rozet = os.getenv("CH_ID_ROZ")
        self.chat_id_vp = os.getenv("CHAT_ID_INFO")
        self.chat_id_sk = os.getenv("CH_ID_SK")
        self.chat_id_confirm = os.getenv("CHAT_ID_CONFIRMATION")
        self.chat_id_cash = os.getenv("CH_ID_CASH")
        self.chat_id_shop = os.getenv("CH_ID_SHOP")
        self.chat_id_courier = os.getenv("CH_ID_CORECTOR")
        if self.env == 'dev':
            self.chat_id_info = os.getenv("CHAT_ID_INFO")
            self.chat_id_np = os.getenv("CHAT_ID_INFO")
            self.chat_id_ukr = os.getenv("CHAT_ID_INFO")
            self.chat_id_rozet = os.getenv("CHAT_ID_INFO")
            self.chat_id_vp = os.getenv("CHAT_ID_INFO")
            self.chat_id_sk = os.getenv("CHAT_ID_INFO")
            self.chat_id_confirm = os.getenv("CHAT_ID_INFO")
            self.chat_id_cash = os.getenv("CHAT_ID_INFO")
            self.chat_id_shop = os.getenv("CHAT_ID_INFO")
            self.chat_id_courier = os.getenv("CHAT_ID_INFO")


    @wrapper()
    def sendMessage(self, chat_id, text, keyboard_json=None):
        if self.env == "dev":
            return self.client.send_message_f("-421982888", text, keyboard_json)
        return self.client.send_message_f(chat_id, text, keyboard_json)
    
    def sendPhoto(self, id_photo):
        chat_list = [self.chat_id_rozet, self.chat_id_np]
        resp = None
        for chat in chat_list:
            resp = self.client.sendPhoto(chat, id_photo)
            print(resp)
        return resp

    def answerCallbackQuery(self, callback_query_id: str, text: str) -> bool:
        resp = self.client.answerCallbackQuery(callback_query_id, text)
        return resp

    def forceReply(self, chat_id, callback_query_id=None, text=None):
        resp = self.client.forceReply(chat_id, callback_query_id, text)
        return resp

    def editMessageText(self, chat_id, message_id, text):
        resp = self.client.editMessageText(chat_id, message_id, text)
        return resp

    def deleteMessage(self, chat_id, message_id):
        resp = self.client.deleteMessage(chat_id, message_id)
        return resp

    def keyboard_func(self):
        resp = self.client.keyboard_func()
        return resp

    def keyboard_generate(self,  text1, callback_data1, text2=None, callback_data2=None):
        resp = self.client.keyboard_generate(text1, callback_data1, text2, callback_data2)
        return resp

    def loadPhoto(self, chat_id):
        return self.client.loadPhoto(chat_id)
    
    def black_pic(self):
        id_photo = 'AgACAgIAAxkBAAIMl2YWFuaONHD9_7SWvzDiiK8vmNQSAAK31jEbGsoISBKbThvzHGUpAQADAgADbQADNAQ'
        resp_photo = self.client.sendPhoto(id_photo)
        if not resp_photo:
            self.logger.info("Телеграм не дал ответа Photo")
        self.logger.info(resp_photo)
        return True