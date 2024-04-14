from .repository import ProductCounBot
from black.telegram_controller import tg_cntrl


pc_cl = ProductCounBot()

class BotProductSrv():
    def work_with_product(self, data):
        text = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]
        print(text)
        update_color = pc_cl.manager_bot(text)
        tg_cntrl.sendMessage(chat_id, update_color)