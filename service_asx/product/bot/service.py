from .repository import ProductCounBot
from telegram import TgClient

tg_cl = TgClient()
pc_cl = ProductCounBot()

class BotProductSrv():
    def work_with_product(self, data):
        text = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]
        print(text)
        update_color = pc_cl.manager_bot(text)
        tg_cl.send_message_f(chat_id, update_color)