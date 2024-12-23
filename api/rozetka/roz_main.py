from utils import BearRequest
# from common_asx.utilits import utils_dev_change

import os, base64
  
  # статуси
  # 1 - новий 
  # 4 доставляєтсья

#     1 Нове замовлення 	
#   2 	# Комплектується. Дані підтверджені 	
#   3 	# Передано в службу доставки 	
#   4 	# Доставляється 	
#   5 	# Чекає в пункті самовивозу 	
#   6 	# Замовлення виконано 	
#  61 	Заплановано передачу перевізникові 	

class RozetMain():
    def __init__(self):
        self.bear_req = BearRequest()
        self.host = "https://api-seller.rozetka.com.ua/"
        self.cash = "Nj2HNztLCMG1pBnr18GtDZ-SSfj4-j5B"

    def get_orders(self):
        prefix = "orders/search?expand=delivery,purchases,payment,status_payment&status=1"
        resp = self.make_request("GET", prefix)
        if "content" in resp:
            if "orders" in resp["content"]:
                if resp["content"]["orders"]:
                    for order in resp["content"]["orders"]:
                        dict_order = self.make_order(order)
                        text = self.make_text(dict_order)
                        return resp
        return None
    
    def authorization(self):
        pass

    
    def change_status_order(self, order_id, status):
        prefix = f"orders/{order_id}"
        body = {
            "status": status
        }
        resp = self.make_request("PUT", prefix, body)
        return resp
    
    def change_ttn_order(self, order_id, ttn, status):
        prefix = f"orders/{order_id}"
        body = {
            "status": status,
            "ttn": ttn
        }
        # resp = utils_dev_change.change_status(body, prefix)
        return resp
    
    def search_data(self, types):
        prefix = "orders/search-data"
        body = {
            "types": types
        }
        # resp = utils_dev_change.change_status(body, prefix)
        return resp
    
    def login(self):
        if not self.cash:
            username = os.getenv("rozet_username")
            password = os.getenv("rozet_password")
            password = base64.b64encode(password.encode("utf-8")).decode("utf-8")
            body = { 
                "username": username,
                "password": password
            }
            # print(body)
            headers = {
                "Content-Type": "application/json"
            }
            resp = self.make_request("POST", "sites", body, headers)
            self.cash = True
            return resp["content"]["access_token"]
        return False
    
    def logout(self):
        prefix = "sites/logout"
        # resp = utils_dev_change.change_status(body, prefix)
        resp = self.make_request("POST", prefix)
        return resp

    def make_request(self, method, prefix, body=None, headers=None):
        url = self.host + prefix
        if not headers:
            headers = {
                "Content-Type": "application/json", "Authorization": f"Bearer {self.cash}"
            }
        print(headers, "headers")
        responce = self.request_go(method, url, headers, body)
        return responce
    
    def request_go(self, method, url, headers, body):
        responce = self.bear_req.request_go(method, url, headers, body)
        # print(method, url, headers, body, "проверка 1 ")
        if responce["success"] == False:
            self.cash = None
            self.cash = self.login()
            headers = {
                "Content-Type": "application/json", "Authorization": f"Bearer {self.cash}"
            }
            if self.cash:
                # print(method, url, headers, body, "проверка")
                responce = self.bear_req.request_go(method, url, headers, body)
        return responce
    
    def make_list_order(self, resp):
        orders = []
        for order in resp["content"]["orders"]:
            dict_order = self.make_order(order)
            orders += self.make_text(dict_order)
        return orders

    def make_order(self, data):
        delivery = data["delivery"]
        purchases = data["purchases"]
        payment = data["payment"]
        return {
            "id": data["id"],
            "user_phone": data["user_phone"],
            "client_firstname": data["user_title"]["first_name"],
            "client_lastname": data["user_title"]["last_name"],
            "client_surname": data["user_title"]["second_name"],
            "recipient_phone": data["recipient_phone"],
            "recipient_firstname": data["recipient_title"]["first_name"],
            "recipient_lastname": data["recipient_title"]["last_name"],
            "recipient_surname": data["recipient_title"]["second_name"],
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
        user_name = order["client_lastname"] + " " + order["client_firstname"]
        recipient = order["recipient_lastname"] + " " + order["recipient_firstname"]
        delivery_option = order["delivery_service_name"]
        delivery_address = "{} ({}) #{} {} - {}".format(
            order["city_name"], order["region"],
            order["place_number"], order["place_street"],
            order["place_house"]
            )
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

        phone_num = order["user_phone"]
        recipient_phone = order["recipient_phone"]
        sum_order = order["amount"]
        formatted_text = ""
        up_text = ""
        for product in all_products:
            up_text += f"{product['artikul']} - {product['quantity']}  - {product['price']} \n"
            formatted_text += f"{product['artikul']} - {product['quantity']}  - {product['price']} \n"
            formatted_text += f"Название: {product['name_multilang']}"

        data_get_order = (
            f"🍎 {up_text} Cумма {sum_order}\n\n{client_notes}\n\n"
            f"{delivery_address}\n\n🍎 Замовлення Розетка Маркет № {order_id}\n\n{phone_num};ТТН немає\nПокупець:\n{user_name}\n\nОтримувач:\n{recipient}\n{recipient_phone}\n{delivery_option}\n"
            f"Способ оплати - {payment_option}, {status} \n\n  На будь якій випадок:\n"
            f"{formatted_text}\n\n=========================================================="
        )
        # print(data_get_order)
        return data_get_order
    
   



            
#     1 	Number 	

# Оплачений
# 2 	Number 	

# Чекає оплату
# 3 	Number 	

# Немає даних
# 4 	Number 	

# Оплачений (LiqPay)
# 5 	Number 	

# Помилка оплати (LiqPay)