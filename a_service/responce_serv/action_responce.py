
from .parse_service import Parse
from utils import my_time
from datetime import datetime

class Command:
    def __init__(self, OrderCntrl, SourAnCntrl):
        self.order_cntrl = OrderCntrl()
        self.SourAnCntrl = SourAnCntrl()
        self.parse = Parse()

    def execute(self, content):
        pass

class Stock(Command):
    def execute(self, data_chat):
        data_chat = self.parse.parse_stock(data_chat, self.SourAnCntrl)
        return data_chat
    
class Take(Command):
    def execute(self, data_chat):
        data_chat = self.parse.parse_stock(data_chat, self.SourAnCntrl)
        return data_chat


class NewOrders(Command):
    def execute(self, data_chat):
        items = self.order_cntrl.load_status_id(10)
        if items:
            for item in items:
                result = self.order_cntrl.send_order_tg(item.id, "⚪️ Нові")
        items = self.order_cntrl.load_status_id(3)
        if items:
            for item in items:
                result = self.order_cntrl.send_order_tg(item.id, "⚪️ Оплачені")
        return None

class AddComment(Command):
    def execute(self, data_chat):
        resp = self.parse.add_comment(data_chat, self.order_cntrl)
        return data_chat
    


class ActionFactory:
    @staticmethod
    def factory(data_chat, OrderCntrl, SourAnCntrl):
        commands = {
            # "take": "take",
            "stock": Stock,
            "new_orders": NewOrders,
            "reply_manager": AddComment,
            "take": Take
        } 
        if data_chat.cmd in commands:
            print("Action Step: ", data_chat.cmd)
            return commands[data_chat.cmd](
                OrderCntrl, SourAnCntrl
                ).execute(data_chat)
        return None