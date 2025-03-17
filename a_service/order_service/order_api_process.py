
import sys
sys.path.append('../')
from common_asx.utilits import Utils


# роутер принимает get_orders та в хідер отримує якій апі

# передає команду в order_api_procces з апі header, 
# OrderApi дивимось якій апі та передаємо обʼєкт апі та визваєм команду

class FactoryApi:
    @staticmethod
    def factory(api, EvoClient, RozetMain):
        apis = {
                "rozetka": RozetMain,
                "prom": EvoClient
        }
        if api in apis:
            return apis[api]()
        else:
            raise ValueError(f"We dont have api: {api}")                
            

class OrderApi:
    def __init__(self, api, OrderCntrl, TG, EvoClient, RozetMain):
        self.api = FactoryApi.factory(api, EvoClient, RozetMain)
        self.order_cntrl = OrderCntrl()
        self.tg = TG()
        self.util = Utils(EvoClient, RozetMain)
    
    def get_orders(self):
        try:
            list_order, list_standart_dto = self.api.get_orders()
            if list_order:
                for order in list_order:
                    text = self.make_text(order)
                    send_tg = self.tg.sendMessage(self.tg.chat_id_confirm, text)
                    print("Send to tg: ", send_tg["ok"])
                    resp = self.util.change_status_rozet(order.id, 26)

                for order in list_standart_dto:
                    resp = self.add_order(order)
                    print("Add to crm: ", resp)
                return True
            return list_standart_dto
        except Exception as e:
            text = f"🔴 Помилка додавання замовлення в розетку {e}"
            return False
        
    def add_order(self, o):
        order_db = self.order_cntrl.add_order2(o)
        if order_db:
            for p in o.ordered_product:
                product_db = self.order_cntrl.add_ordered_product(p, order_db.id)
            return True if product_db else False
        return False 

    def change_status(self, order_id, status):
        resp =self.api.create_status_get(order_id, status)        
        return resp

    def get_order(self, order_id):
        order_dr = self.api.get_order_id(order_id)
        return order_dr

    def send_ttn(self, order_id, invoice_n, delivery):
        dict_ = self.prom_serv.dict_invoice(order_id, invoice_n, delivery)
        resp = self.utils.change_ttn(dict_)
        return resp
        
    def get_delivery(self):
        self.api.available_delivery()
        return True
    
            
    def make_text(self, order):
        user_name = f"{order.user_title.last_name} {order.user_title.first_name}"
        recipient = f"{order.recipient_title.last_name} {order.recipient_title.first_name}"
        delivery_address = (            
            f"{order.delivery.city.city_name} "
            f"({order.delivery.city.region_title}) "
            f"{order.delivery.place_number} "
            f"{order.delivery.place_street}, "
            f"{order.delivery.place_house}"
            )
        dev_text = (
                 f"delivery_service_id: {order.delivery.delivery_service_id}\n"
            f"payment_method_id: {order.payment.payment_method_id}\n"
            f"delivery_method_id: {order.delivery.delivery_method_id}\n"
        )
        payment_option = order.payment.payment_method_name
        client_notes = f"💬 Нотатка: {order.comment}" if order.comment else "Нотаток від клієнта нема"
        status = order.status_payment if order.status_payment else order.payment.payment_type_title
        products = "\n".join([f"{p.item.article} - {p.quantity} - {p.price}\n" for p in order.purchases])
        products_info = "\n".join([f"Назва: {p.item.name_ua}\n" for p in order.purchases])     
        sum_order = order.amount_with_discount
        phone_num = order.user_phone
        recipient_phone = order.recipient_phone
        return (
            f"🟢 {products} Cумма {sum_order}\n\n"
            f"Дата створення замовлення {order.created}\n\n"
            f"{client_notes}\n\n"
            f"{order.delivery.delivery_service_name}\n"
            f"{payment_option}, {status}\n"
            f"Покупець:\n{user_name}\n{phone_num};ТТН\n\n"
            f"🟢 Замовлення Розетка Маркет № {order.id}\n\n"
            f"Отримувач:\n{delivery_address}\n"
            f"{recipient}\n{recipient_phone}\n\n"
            f"{products_info}\n"
            f"{dev_text}\n"
            "=========================================================="
        )





