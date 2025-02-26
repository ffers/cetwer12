
from .parse_service import Parse
from utils import my_time
from datetime import datetime

class Command:
    def __init__(self, OrderCntrl, SourAnCntrl):
        self.order = OrderCntrl()
        self.SourAnCntrl = SourAnCntrl()

    def execute(self, content):
        pass

class AddtoBaseCommand(Command):
    def execute(self, data_chat):
        data_chat.resp = []
        for item in data_chat.content:
            article = item["article"] 
            quantity = self.quantity_parse(item)
            item = self.SourAnCntrl.load_article(article)
            if not item:
                quantity = "Нема такого товару"
            else:
                # event_time = datetime.strptime(next(my_time()), "%a %b %Y")
                # print(event_time)
                resp = self.SourAnCntrl.fixed_process(item.id, quantity, data_chat.comment)               
            pointer = self.parser_item(data_chat, article, quantity)    
        return data_chat
    
    def quantity_parse(self, item):
        if "data" in item:
            return Parse().all_color(item["data"])
        return item["quantity"]

    def parser_item(self, data_chat, article, quantity):
        data_chat.resp.append({
            "article": article,
            "quantity": quantity
        })
        return data_chat


class NewOrders(Command):
    def execute(self, data_chat):
        items = self.order.load_status_id(10)
        if items:
            for item in items:
                result = self.order.send_order_tg(item.id, "⚪️ Нові")
        items = self.order.load_status_id(3)
        if items:
            for item in items:
                result = self.order.send_order_tg(item.id, "⚪️ Оплачені")
        return None




class ActionFactory:
    @staticmethod
    def factory(data_chat, OrderCntrl, SourAnCntrl):
        commands = {
            # "take": "take",
            "stock": AddtoBaseCommand,
            "new_orders": NewOrders
        } 
        if data_chat.cmd in commands:
            return commands[data_chat.cmd](
                OrderCntrl, SourAnCntrl
                ).execute(data_chat)
        return None