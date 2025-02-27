from utils import my_time
from datetime import datetime


class Parse:
    def __init__(self):
        pass

    def all_color(self, items):
        sum = 0
        for a,b in items.items():
            sum += b
        return sum
    
    def quantity_parse(self, item):
        if "data" in item:
            return self.all_color(item["data"])
        return item["quantity"]

    def parser_item(self, data_chat, article, quantity):
        data_chat.resp.append({
            "article": article,
            "quantity": quantity
        })
        return data_chat
    
    def add_comment(self, data_chat, order_cntrl):
        time = next(my_time()).strftime("%d-%m-%Y %H:%M")
        comment = time + ": " + data_chat.comment
        order = order_cntrl.load_for_order_code(data_chat.text)
        add_comment = order_cntrl.update_history(order.id, comment)
        print(add_comment, "update_history")
        return add_comment
