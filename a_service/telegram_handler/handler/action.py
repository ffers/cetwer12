
from .parsers.parse_worker import Parse
from utils import my_time
from datetime import datetime
from .action_v2.actions.stock_action import StockAction

class Command:
    def __init__(self, **deps):
        self.order_cntrl = deps["OrderCntrl"]()
        self.SourAnCntrl = deps["SourAnCntrl"]()
        self.order_serv = deps["OrderServ"]()
        self.parse = Parse()     

    def execute(self, content):     
        pass      
     
class Take(Command):
    def execute(self, data_chat): 
        return data_chat
    
# class Stock(Command):
#     def execute(self, data_chat):
#         data_chat = self.parse.parse_stock(data_chat, self.SourAnCntrl)
#         return data_chat 
       
      
        
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
        print("AddComment:", resp)
        return data_chat
    
class UnknownCommandAction(Command):
    def execute(self, data_chat):
        return data_chat
    
    '''
    тількі ордеркод, якшо співпадає з 4 варіантів то шукаєм
    унікальне замовленя
    '''
class SearchOrder(Command):
    def execute(self, data_chat):
        n = data_chat.text
        result = self.order_serv.search_order_6_number(n)
        data_chat.content = result  
        return data_chat


class Action:
    @staticmethod
    def factory(data_chat, **deps):
        commands = {
            "stock": StockAction,
            "new_orders": NewOrders,
            "reply_manager": AddComment,
            "take": Take,
            "take_courier": StockAction,
            "unknown_command": UnknownCommandAction,
            "search_order_manager": SearchOrder
        } 
        if data_chat.cmd in commands:
            print("Action Step: ", data_chat.cmd)
            return commands[data_chat.cmd](
                **deps
                ).execute(data_chat)
        return data_chat