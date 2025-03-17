from datetime import datetime
from a_service.order_service.order_api_process import OrderApi


class GetOrder:
    def __init__(self, api):
        self.service = OrderApi(
            api,
            OrderCntrl, 
            TelegramController
        )
    
    def get_orders(self):
         return self.service.get_orders()
    
    def change_status(self):
        return self.change_status()