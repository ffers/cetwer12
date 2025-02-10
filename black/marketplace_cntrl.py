from api import EvoClient, RozetMain
from .telegram_controller import TelegramController
from .order_cntrl import OrderCntrl
from dataclasses import dataclass, field



import sys, os
sys.path.append('../')
from common_asx.utilits import Utils

class MarketFactory:
    @staticmethod
    def factory(condition):
        match condition:
            case "prom": 
                token = os.getenv("token_prom")
                return EvoClient(token) 
            case "rozetka": 
                return RozetMain()
            case _: 
                return ValueError(f"Неизвестный маркетплейс: {condition}")




@dataclass
class MarketplaceCntrl:
    tg: TelegramController = field(default_factory=TelegramController)
    util: Utils = field(default_factory=Utils)
    order_cntrl: OrderCntrl = field(default_factory=OrderCntrl)
    
    def get_orders(self):
        try:
            list_order, list_standart_dto = self.marketplats.get_orders()
            if list_order:
                for order in list_order:
                    text = self.make_text(order)
                    send_tg = self.tg.sendMessage(self.tg.chat_id_confirm, text)
                    print(order.id, "order id")
                    resp = self.util.change_status_rozet(order.id, 26)

                for order in list_standart_dto:
                    resp = self.add_order(order)
                    print(resp)
                return True
            return False
        except Exception as e:
            text = f"🔴 Помилка додавання замовлення в розетку {e}"
            return self.tg.sendMessage(self.tg.chat_id_info, text)

    def add_order(self, o):
        order_db = self.order_cntrl.add_order2(o)
        if order_db:
            for p in o.ordered_product:
                product_db = self.order_cntrl.add_ordered_product(p, order_db.id)
                return True if product_db else False
        return False 
        
    def change_status(self, order_id, status):
        resp =self.marketplats.create_status_get(order_id, status)        
        return resp

    def get_order(self, order_id):
        order_dr = self.marketplats.get_order_id(order_id)
        return order_dr

    def send_ttn(self, order_id, invoice_n, delivery):
        dict_ = self.prom_serv.dict_invoice(order_id, invoice_n, delivery)
        resp = utils_dev_change.change_ttn(dict_)
        return resp

    def init_class(self, condition):
        if condition == "Rozet":
            return RozetMain()
        elif condition == "Prom":
            return prom_api
        else:
            raise ValueError("Невідомий тип платформи")
        
    def get_delivery(self):
        self.marketplats.available_delivery()
        return True
    
    def other_actions(self, **kwargs):
        raise NotImplementedError
            
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





