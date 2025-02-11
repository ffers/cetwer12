from datetime import datetime
from a_service.order_service.order_api_process import RozetkaMarketFactory, PromMarketFactory
from ..order_cntrl import OrderCntrl
from ..telegram_controller import TelegramController

# Базовий клас замовлення
# class Controller:
#     def __init__(self, type_process):
#         self.type_process = type_process

#     def process(self):
#         raise NotImplementedError("Subclasses must implement process()")

# # Класи для кожного статусу
# class GetOrders(Controller):
#     def process(self, type_process):
#         return MarketFactory.factory(type_process, OrderCntrl, TelegramController) 

# class ChangeStatus(Controller):
#     def process(self, type_process):
#         return MarketFactory.factory(type_process, OrderCntrl, TelegramController) 


# # Фабричний метод для створення замовлення за статусом
# class ControllerFactory:
#     @staticmethod
#     def get_orders(type_api, type_process):
#         order_classes = {
#             "get_orders": GetOrders,
#             "change_status": ChangeStatus
#         }
#         if type_api in order_classes:
#             return order_classes[type_api](type_process)
#         else:
#             raise ValueError(f"Unknown order status: {type_api}")\

# 
class Handler:
    """Базовый обработчик цепочки обязанностей"""
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler  # Позволяет делать цепочку вызовов

    def handle(self, api, task):
        if self.next_handler:
            return self.next_handler.handle(api, task)
        raise ValueError(f"❌ No handler found for API: {api}, Task: {task}")
    

class PromAPIHandler(Handler):
    def handle(self, api, task):
        if api == "prom":
            return PromMarketFactory.factory(task).process()
        return super().handle(api, task)

class RozetkaAPIHandler(Handler):
    def handle(self, api, task):
        if api == "rozetka":
            return RozetkaMarketFactory.factory(task, OrderCntrl, TelegramController).process()
        return super().handle(api, task)


