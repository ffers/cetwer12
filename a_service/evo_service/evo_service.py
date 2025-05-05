from api import EvoClient
import re
from application.handlers import OrderHandler, ContextHandler



class EvoService:
    def __init__(self, evo_api: EvoClient):
        self.evo_api = evo_api 
        self.pipline = (
            OrderHandler()
            .add_command
            )

 
    def get_orders(self):
        return self.evo_api.get_orders()
    
    def get_order(self, order_id):
        order_id = re.sub(r"\D", "", order_id)
        return self.evo_api.get_order(order_id)
    
    def change_status(self, order_id, status):
        return self.evo_api.change_status(order_id, status) # добавить dev
    
    def send_ttn(self, order_id, invoice_n, delivery):
        return self.evo_api.send_ttn(order_id, invoice_n, delivery)