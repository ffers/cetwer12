from a_service import TgCashServ
from black.sour_an_cntrl import SourAnCntrl
from black.telegram_controller import TelegramController

class TgCashCntrl:
    def __init__(self):
        self.serv = TgCashServ()
        self.source = SourAnCntrl()
        self.cntrl = TelegramController()

    def text_f(self, data):
        if "text" in data["message"]:
            return data["message"]["text"]
        else:
            return "None"

    def sort(self, data):
        text = self.text_f(data)
        if "#add" in text:
            self.add_f(text)
        elif "#quan" in text:
            self.quan_f(text)

    def add_f(self, text):
        data_dict = self.serv.arrival(text)
        print(data_dict)
        if data_dict:
            for item in data_dict:
                article = item["article"]
                quantity = item["quantity"]
                description = item["description"]
                resp, new_quantity = self.source.stock_journal(article, int(quantity), description)
                print(resp)
                self.cntrl.sendMessage(self.cntrl.chat_id_cash, new_quantity)
            return True, 200
        else:
            return False, 200

    def quan_f(self, text):
        articles = self.serv.quan_f(text)
        text = ''
        if articles:
            for article in articles:
                quan = self.source.rep.load_article(article["article"])
                print(quan)
                if quan:
                    text += f"{quan.article}={quan.quantity}\n"
            print(text)
            self.cntrl.sendMessage(self.cntrl.chat_id_cash, text)
        else:
            print(False)
            return False







