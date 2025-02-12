from datetime import datetime
from a_service.order_service.order_api_process import OrderApi
from ..order_cntrl import OrderCntrl
from ..telegram_controller import TelegramController

class GetOrder:
    def __init__(self, api):
        self.api = api
        self.service = OrderApi(
            self.api,
            OrderCntrl, 
            TelegramController
        )
    
    def get_orders(self):
         return self.service.get_orders()
    
    def change_status(self):
        return self.change_status()