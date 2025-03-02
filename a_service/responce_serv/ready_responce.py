
from .parse_service import Parse
from utils import my_time
from datetime import datetime

class Command:
    def __init__(self, OrderCntrl, SourAnCntrl, TelegramCntrl):
        self.OrderCntrl = OrderCntrl()
        self.SourAnCntrl = SourAnCntrl()
        self.tg = TelegramCntrl()

    def execute(self, pointer):
        pass 

class ResponceCommand(Command):
    def execute(self, pointer):
        print(pointer, "ResponceCommand")
        if pointer.resp:
            pointer = self.parse(pointer)
            resp = self.tg.sendMessage(self.tg.chat_id_courier, pointer.text)
            return f"додано Ярік {resp}"
        else:
            self.tg.sendMessage(self.tg.chat_id_courier, "Невірна команда")
        return None   

    def parse(self, pointer):
        pointer.text = pointer.comment
        for item in pointer.resp:
            pointer.text += "{}: {}\n".format(
                item["article"], 
                item["quantity"]
                )
        return pointer
 
class ReadyFactory:
    @staticmethod
    def factory(pointer, OrderCntrl, SourAnCntrl, TelegramCntrl):
        commands = {
            # "take": "take",
            "stock": ResponceCommand,
            # "edit": "edit",
            # "arrival": "ArrivalCommand,",
            # "comment":"comment"
        } 
        if pointer.cmd in commands:
            return commands[pointer.cmd](
                OrderCntrl, SourAnCntrl, TelegramCntrl
                ).execute(pointer)
        return None