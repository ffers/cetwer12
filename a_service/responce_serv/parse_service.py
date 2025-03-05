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
    

    
    def add_comment(self, data_chat, order_cntrl):
        time = next(my_time()).strftime("%d-%m-%Y %H:%M")
        comment = time + ": " + data_chat.comment
        order = order_cntrl.load_for_order_code(data_chat.text)
        add_comment = order_cntrl.update_history(order.id, comment)
        return add_comment
    
    def quantity_parse(self, item, data_chat):
        if "data" in item:
            return self.all_color(item["data"])
        if data_chat.cmd == "take": 
            return -item["quantity"]
        return item["quantity"]
    
    def parser_item(self, data_chat, article, quantity):
        data_chat.resp.append({
            "article": article,
            "quantity": quantity
        })
        return data_chat 
     
    def parse_stock(self, data_chat, sour_cntrl):
        data_chat.resp = [] 
        for item in data_chat.content:
            quantity = "Нема такого товару"
            item_prod = sour_cntrl.load_article(item["article"])
            if item_prod:
                quantity = self.quantity_parse(item, data_chat)
                print("dev_parse_color: ", data_chat.comment)
                sour_cntrl.fixed_process(item_prod.id, quantity, data_chat.comment, next(my_time()))               
            data_chat = self.parser_item(data_chat, item["article"], quantity)   
        return data_chat