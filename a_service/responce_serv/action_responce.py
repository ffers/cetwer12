
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
        for item in data_chat.content:
            article = item["article"] 
            quantity = Parse().all_color(item["data"])
            item = self.SourAnCntrl.load_article(article)
            # event_time = datetime.strptime(next(my_time()), "%a %b %Y")
            # print(event_time)
            resp = self.SourAnCntrl.fixed_process(item.id, quantity, "Приход Ярік")
            if resp:
                item = self.SourAnCntrl.load_article(article)
                pointer = self.parser_item(data_chat, article, quantity) 
               
        return pointer
    
    def parser_item(self, pointer, article, quantity):
        pointer.resp = [{
            "article": article,
            "quantity": quantity
        }]
        return pointer


class NewOrders(Command):
    def execute(self, data_chat):
        items = self.order.load_status_id(10)
        print(items)
        for item in items:
            result = self.order.send_order_tg(item.id, "⚪️ Нові")
            print(result)
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