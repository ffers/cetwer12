
from utils import my_time
from datetime import datetime
from .parsers import ParseResponce

class Command:
    def __init__(self, OrderCntrl, SourAnCntrl, TelegramCntrl):
        self.OrderCntrl = OrderCntrl()
        self.SourAnCntrl = SourAnCntrl()
        self.tg = TelegramCntrl()
        self.parser = ParseResponce()

    def execute(self, pointer):
        pass 

class ResponceCommand(Command):
    def execute(self, pointer):
        if pointer.resp:
            pointer = self.parser.text_report_add(pointer)
            resp = self.tg.sendMessage(self.tg.chat_id_courier, pointer.text)
            return f"додано Ярік {resp}"
        else:
            self.tg.sendMessage(self.tg.chat_id_courier, "Неправильно сформульоване повідомлення")
        return pointer 

class UnknownCommandResponce(Command):
    def execute(self, pointer):
        if pointer.resp:
            pointer = self.parser.text_unknown_command(pointer)
            resp = self.tg.sendMessage(self.tg.chat_id_courier, pointer.text)
            return pointer


 
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