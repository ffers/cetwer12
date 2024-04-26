from a_service import TgArrivalServ
from black.sour_an_cntrl import SourAnCntrl
from black.telegram_controller import TelegramController

class TgArrivalCntrl:
    def __init__(self):
        self.serv = TgArrivalServ()
        self.source = SourAnCntrl()
        self.cntrl = TelegramController()


    def sort(self, data):
        text = self.text_f(data)
        if "#add" in text:
            self.add(text)
        elif "#quan" in text:
            pass

    def add(self, text):
        data_dict = self.serv.article(text)
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
        article = None
        quan = self.source.rep.load_article(article)
        self.cntrl.sendMessage(self.cntrl.chat_id_cash, quan)



    def text_f(self, data):
        text = data["message"]["text"]
        print(text)
        return text



