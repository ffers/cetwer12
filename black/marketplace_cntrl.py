from a_service import prom_serv
from api import prom_api, RozetMain
from .telegram_controller import TelegramController

import sys
sys.path.append('../')
from common_asx.utilits import utils_dev_change


class MarketplaceCntrl:
    def __init__(self, condition):
        self.marketplats = self.init_class(condition)
        self.tg = TelegramController()
    
    def change_status(self, order_id, status):
        resp =self.marketplats.create_status_get(order_id, status)        
        return resp

    def get_order(self, order_id):
        order_dr = self.marketplats.get_order_id(order_id)
        return order_dr

    def send_ttn(self, order_id, invoice_n, delivery):
        dict_ = prom_serv.dict_invoice(order_id, invoice_n, delivery)
        resp = utils_dev_change.change_ttn(dict_)
        return resp

    def init_class(self, condition):
        if condition == "Rozet":
            return RozetMain()
        elif condition == "Prom":
            return prom_api
        else:
            raise ValueError("Невідомий тип платформи")
        
    def get_orders(self):
        try:
            data = self.marketplats.get_orders()
            if data:
                for order in data["content"]["orders"]:
                    dict_order = self.make_order(order)
                    text = self.make_text(dict_order)
                    send_tg = self.tg.sendMessage(self.tg.chat_id_confirm, text)
                    self.marketplats.change_status_order(dict_order["id"], 26)
                return True
            return False
        except:
            return False

    

    def make_order(self, data):
        delivery = data["delivery"]
        purchases = data["purchases"]
        payment = data["payment"]
        return {
            "id": data["id"],
            "phone": data["recipient_phone"],
            "client_firstname": data["recipient_title"]["first_name"],
            "client_lastname": data["recipient_title"]["last_name"],
            "client_surname": data["recipient_title"]["second_name"],
            "another_recipient": False,
            "delivery_service_id": 
                self.delivery_service_id(delivery["delivery_service_id"]),
            "delivery_service_name": delivery["delivery_service_name"],
            "city_name": delivery["city"]["city_name"],
            "city_ref": delivery["city"]["uuid"],
            "region": delivery["city"]["region_title"],
            "delivery_method_id": delivery["delivery_method_id"],
            "place_street": delivery["place_street"],
            "place_number": delivery["place_number"],
            "place_house": delivery["place_house"],
            "place_flat": delivery["place_flat"],
            "warehouse_ref": delivery["ref_id"],
            "payment_option": payment["payment_method_name"],
            "payment_status": payment["payment_status"],
            "ordered_product": purchases,
            "amount": data["amount"],
            "sum_price": data["amount"],
            
            "description": data["comment"],
            "description_delivery": data["user_title"],
            "cpa_commission": data["user_title"],
            "client_id": data["user_title"],
            "order_code": data["user_title"],
            "warehouse_method_id": data["user_title"],
            "source_order_id": data["user_title"],
            "payment_method_id": data["user_title"],
            "delivery_method_id": data["user_title"],
            "pickup_rz_id":data["delivery"]["pickup_rz_id"],
            "area":""
        }
 
    
    def make_text(self, order):
        order_id = order["id"]
        client_name = order["client_lastname"] + " " + order["client_firstname"]
        delivery_option = order["delivery_service_name"]
        delivery_address = "{} {} #{}".format(order["city_name"], order["region"], order["place_number"])
        payment_option = order["payment_option"]
        full_price = order["amount"]
        if "description" in order and order["description"]:
            client_notes = "Нотатка: " + order["client_notes"]
        else:
            client_notes = "Нотаток від клієнта нема"
        status = order["payment_status"]
        all_products = []
        for sku in order["ordered_product"]:
            item = sku["item"]
            product = {
                "artikul": item["article"],
                "name_multilang": item["name_ua"],
                "price": item["price"],
                "quantity": sku["quantity"],
                # "measure_unit": sku["measure_unit"],
                # "image_url": sku["image"],
                "total_price": sku["cost"]
            }
            all_products.append(product)

        phone_num = order["phone"]
        sum_order = order["amount"]
        formatted_text = ""
        up_text = ""
        for product in all_products:
            up_text += f"{product['artikul']} - {product['quantity']}  - {product['price']} \n"
            formatted_text += f"{product['artikul']} - {product['quantity']}  - {product['price']} \n"
            formatted_text += f"Название: {product['name_multilang']}"

        data_get_order = (
            f"🍎 {up_text} Cумма {sum_order}\n\n{client_notes}\n\n"
            f"{delivery_address}\n\n🍎 Замовлення Розетка Маркет № {order_id}\n\n{phone_num};ТТН немає\n{client_name}\n{delivery_option}\n"
            f"Способ оплати - {payment_option}, {status} \n\n  На будь якій випадок:\n"
            f"{formatted_text}\n\n=========================================================="
        )
        # print(data_get_order)
        return data_get_order

    def delivery_service_id(self, id):
        if id == 5:
            method = 1
        elif id == 4:
            method = 1
        elif id == 2024:
            method = 1
        elif id == 2:
            method = 1
        elif id == 1:
            method = 1
        else:
            return print("Нема доступних методів пошти")
        return method
    
    def payment_method_id(self, id):
        if id == 5:
            method = 1
        elif id == 4:
            method = 1
        elif id == 3:
            id = 1
        elif id == 2:
            method = 1
        elif id == 1:
            method = 1
        else:
            return print("Нема доступних методів оплати")
        return method
    




