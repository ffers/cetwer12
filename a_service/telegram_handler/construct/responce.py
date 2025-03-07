
from utils import my_time
from datetime import datetime
from .parsers import ParseResponce

class Command:
    def __init__(self, OrderCntrl, SourAnCntrl, TelegramCntrl):
        self.OrderCntrl = OrderCntrl()
        self.SourAnCntrl = SourAnCntrl()
        self.tg = TelegramCntrl()
        self.parser = ParseResponce()

    def sendMessage(self, data_chat):
        resp = self.tg.sendMessage(data_chat.chat_nummer, data_chat.text)
        print(resp)
        if resp:
            print("Telegram result: ", resp["ok"])

    def execute(self, pointer):
        pass 

class ResponceCommand(Command):
    def execute(self, data_chat):
        if data_chat.resp:
            data_chat = self.parser.text_report_add(data_chat)
            resp = self.tg.sendMessage(self.tg.chat_id_courier, data_chat.text)
            return f"додано Ярік {resp}"
        else:
            self.tg.sendMessage(self.tg.chat_id_courier, "Неправильно сформульоване повідомлення")
        return data_chat 

class UnknownCommandResponce(Command):
    def execute(self, data_chat):
        data_chat = self.parser.text_unknown_command(data_chat)
        self.sendMessage(data_chat)
        return data_chat


 
class ResponceFactory:
    @staticmethod
    def factory(pointer, OrderCntrl, SourAnCntrl, TelegramCntrl):
        commands = {
            "take": ResponceCommand, 
            "stock": ResponceCommand,
            "unknown_command": UnknownCommandResponce
            # "edit": "edit",
            # "arrival": "ArrivalCommand,",
            # "comment":"comment"
        } 
        if pointer.cmd in commands:
            return commands[pointer.cmd](
                OrderCntrl, SourAnCntrl, TelegramCntrl
                ).execute(pointer)
        return pointer