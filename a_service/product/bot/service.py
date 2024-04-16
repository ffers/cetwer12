from .repository import ProductCounBot

pc_cl = ProductCounBot()

class BotProductSrv():
    def work_with_product(self, data):
        text = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]
        print(text)
        update_color = pc_cl.manager_bot(text)
        return update_color