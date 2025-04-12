from utils import my_time
from datetime import datetime
from utils import handle_error

class Parse:                                 
    def __init__(self): 
        pass
  
    def all_color(self, items):     
        sum = 0
        for a,b in items.items():                      
            sum += b 
        return sum
    
    def add_comment(self, data_chat, order_cntrl):
        comment = f"{data_chat.comment} ({data_chat.author})"
        order = order_cntrl.load_for_order_code(data_chat.text)
        if order:
            print("Order:", order)
            return order_cntrl.update_history(order.id, comment)
        return False
    
    # def quantity_parse(self, item, data_chat):
    #     if "data" in item:
    #         return self.all_color(item["data"])
        # if data_chat.cmd == "take_courier": 
        #     return -item["quantity"]
        # return item["quantity"]
    
    def parser_item(self, data_chat, article, quantity):
        data_chat.resp.append({
            "article": article,
            "quantity": quantity
        })
        return data_chat      
     
    def parse_stock(self, data_chat, sour_cntrl):
        data_chat.resp = [] 
        for item in data_chat.content:
            try:
                quantity = "Нема такого товару"
                item_prod = sour_cntrl.load_article(item["article"])
                if item_prod:
                    quantity = item["quantity"]
                    print("parse_stock:", data_chat)
                    if not data_chat.comment:
                        raise ValueError("Некоректний шаблон")
                    print("dev_parse_color: ", data_chat.comment)
                    sour_cntrl.fixed_process(item_prod.id, quantity, data_chat.comment, next(my_time()))               
                data_chat = self.parser_item(data_chat, item["article"], quantity)
            except Exception as e:
                print(f"Помилка під час обробки '{item}': {e}")                
                data_chat.text = f"{e}\n"
                data_chat = self.parser_item(
                    data_chat, item.get("article", "?"), "Нерахується"
                )
                break
                
        return data_chat 