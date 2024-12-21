from utils import BearRequest
# from common_asx.utilits import utils_dev_change

import os, base64
  

class RozetMain():
    def __init__(self):
        self.bear_req = BearRequest()
        self.host = "https://api-seller.rozetka.com.ua/"
        self.cash = "-aSPwaMa0OFmaXKPnECvVYSqU6F2MrX5"

    def get_orders(self):
        prefix = "orders/search?expand=delivery,purchases,payment,status_payment&status=1"
        resp = self.make_request("GET", prefix)
        if resp["content"]["orders"]:
            json_order = resp
            return json_order
        return None
    
    def authorization(self):
        pass

    
    def change_status_order(self, order_id, status):
        url = f"https://api-seller.rozetka.com.ua/orders/{order_id}"
        body = {
            "status": status
        }
        # resp = utils_dev_change.change_status(body, url)
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
            print(body)
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
        print(headers)
        responce = self.request_go(method, url, headers, body)
        return responce
    
    def request_go(self, method, url, headers, body):
        responce = self.bear_req.request_go(method, url, headers, body)
        print(method, url, headers, body, "проверка 1 ")
        if responce["success"] == False:
            self.cash = None
            self.token = self.login()
            if self.token:
                print(method, url, headers, body, "проверка")
                responce = self.bear_req.request_go(method, url, headers, body)
        return responce
    
    def make_order(self, data):
        return {
            "id": data["id"],
            "phone": data["user_phone"],
            "client_firstname": data["user_title"]["first_name"],
            "client_lastname": data["user_title"]["last_name"],
            "client_surname": data["user_title"]["second_name"],
            "another_recipient": False,
            "delivery_service_id": 
                self.delivery_service_id(data["delivery"]["delivery_service_id"]),
            "city_name": data["city"]["city_name"],
            "city_ref": data["city"]["uuid"],
            "region": data["city"]["region_title"],
            "delivery_method_id": data["delivery_method_id"],
            "place_street": data["place_street"],
            "place_number": data["place_number"],
            "place_house": data["place_house"],
            "place_flat": data["place_flat"],
            "warehouse_ref": data["ref_id"],
            "payment_option": None,
            "ordered_product": data["user_title"],
            "sum_price": data["user_title"],
            "sum_before_goods": data["user_title"],
            "description": data["user_title"],
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
    
    def delivery_service_id(self, id):
        if id == 5:
            method = 1
        elif id == 4:
            method = 1
        elif id == 3:
            method = 1
        elif id == 2:
            method = 1
        elif id == 1:
            method = 1
        else:
            return print("Нема доступних методів")
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
            return print("Нема доступних методів")
        return method



            
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