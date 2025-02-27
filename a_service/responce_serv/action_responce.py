
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

class AddtoBaseCommand(Command):
    def execute(self, data_chat):
        data_chat.resp = []
        for item in data_chat.content:
            quantity = "Нема такого товару"
            item_prod = self.SourAnCntrl.load_article(item["article"])
            if item_prod:
                quantity = self.parse.quantity_parse(item)
                self.SourAnCntrl.fixed_process(item_prod.id, quantity, data_chat.comment, next(my_time()))               
            data_chat = self.parse.parser_item(data_chat, item["article"], quantity)    
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
            "stock": AddtoBaseCommand,
            "new_orders": NewOrders,
            "reply_manager": AddComment,
        } 
        if data_chat.cmd in commands:
            return commands[data_chat.cmd](
                OrderCntrl, SourAnCntrl
                ).execute(data_chat)
        return None