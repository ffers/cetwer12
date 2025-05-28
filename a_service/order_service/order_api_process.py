
import re, os


# роутер принимает get_orders та в хідер отримує якій апі

# передає команду в order_api_procces з апі header, 
# OrderApi дивимось якій апі та передаємо обʼєкт апі та визваєм команду

'''
Отслеживания изменений только по принятим заказам, 
если они виполнени или отправлени 
нет смисла отслеживать изменения
те вопроси которих  не касается человек должна 
касаться машина
Загружаєм принятие закази
по каждому где нет send_time заказу
по каждому заказу сайта сравниваем изменения по статусу
по каждому заказу промоплати и неоплачено сравниваем статус оплати
'''          
            

class OrderApi:
    def __init__(self, api):
        self.api = api
    
    def get_orders(self):
        list_order = self.api.get_orders()
        return list_order
     

    def change_status(self, order_id, status):
        env = os.getenv("ENV")
        if env != "dev":
            order_id = re.sub(r"\D", "", order_id)
            return self.api.change_status(order_id, status) 
        return {"status": "dev"}   


    def get_order(self, order_id):
        order_id = re.sub(r"\D", "", order_id)
        return self.api.get_order_id(order_id)
        

    def send_ttn(self, order_id, invoice_n, delivery):
        order_id = re.sub(r"\D", "", order_id)
        return self.api.send_ttn(order_id, invoice_n, delivery)
        
    def get_delivery(self):
        self.api.available_delivery()
        return True
   
