



from utils import my_time
from datetime import datetime
from ..parsers import ParseResponce

class Command:
    def __init__(self, **deps):
        self.tg = deps["TelegramCntrl"]()
        self.text = deps["TextFormat"]
        self.parser = ParseResponce()

    def sendMessage(self, data_chat):
        resp = self.tg.sendMessage(data_chat.chat_nummer, data_chat.text)
        print(resp)
        if resp:
            print("Telegram result: ", resp["ok"])

    def execute(self, pointer):
        pass 