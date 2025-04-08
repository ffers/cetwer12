


from datetime import datetime
from .statuses import *

class Order:
    def __init__(self, order_id, status, tg_serv, ord_rep):
        self.order_id = order_id
        self.status = 10
        self.created_at = datetime.now()
        self.tg_serv = tg_serv()
        self.ord_rep = ord_rep()
        


    def process(self):
        raise NotImplementedError("Subclasses must implement process()")

class PaidOrder(Order):
    def process(self):
        return f"💳 Order {self.order_id} is paid and ready for shipping."

class ShippedOrder(Order):
    def process(self):
        return f"🚚 Order {self.order_id} has been shipped."

class DeliveredOrder(Order):
    def process(self):
        return f"📦 Order {self.order_id} delivered to {self.customer}."

class PreOrder(Order):
    def process(self):
        order = self.ord_rep.load_item(self.order_id)
        data_tg_dict = self.tg_serv.create_text_order(order)
        keyboard_json = self.tg_serv.keyboard_func()
        print("PreOrder")
        self.tg_cntrl.sendMessage(self.tg_cntrl.chat_id_shop, data_tg_dict, keyboard_json)
        return f"📦 Order create and send to shop group"
    
class PassOrder(Order):
    def process(self):
        pass

# Фабричний метод для створення замовлення за статусом
class StatusProcess:
    @staticmethod
    def factory(order_id: int, status: int, tg_serv, ord_rep):
        print("StatusProcess factory ", order_id, status)
        order_classes = {
            1: PassOrder, 2: ConfirmedOrder, 
            3: PassOrder, 4: PassOrder,
            5: PassOrder, 6: PreOrder, 
            7: PassOrder, 8: PassOrder,
            9: PassOrder, 10: PassOrder, 
            11: PassOrder, 12: PassOrder,
            13: PassOrder, 14: PassOrder,
            15: PassOrder
        }
        
        if status in order_classes:
            print("search dict")
            return order_classes[status](order_id, status, tg_serv, ord_rep).process()
        
        raise ValueError(f"Unknown order status: {status}")

            
# <option value="1">Підтвердити</option>
# <option value="2">Підтвержено</option>
# <option value="3">Оплачено</option> 
# <option value="4">Несплачено</option>
# <option value="5">Скасовано</option>
# <option value="6">Предзамовлення</option>
# <option value="7">Питання</option>
# <option value="8">Відправлено</option>
# <option value="9">Отримано</option>
# <option value="10">Нове</option>
# <option value="11">Очікує відправленя</option>
# <option value="12">Виконано</option>
# <option value="13">Тест</option>
        
            
        

# order1 = StatusProcess.update_order(1, 6, "TG")

# print(order1.process())