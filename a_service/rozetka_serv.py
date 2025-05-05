from api import RozetMain

from application.handlers import OrderHandler, ContextHandler



class RozetkaServ:
    def __init__(self, rozetka: RozetMain):
        self.rozetka = rozetka 
        self.pipline = (
            OrderHandler()
            .add_command
            )

 
    def get_orders(self):
        return self.rozetka.get_orders()
    
    def change_status(self, order_id, status):
        return self.rozetka.change_status(order_id, status) # добавить dev
    
    def send_ttn(self, order_id, invoice_n, delivery):
        return self.rozetka.send_ttn(order_id, invoice_n, delivery)