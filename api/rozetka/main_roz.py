from utils import BearRequest
from DTO import OrderRozetkaDTO

import os, base64
from a_service import TokenRepServ
from utils import Stub 
  
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
#  26 "Обробляється менеджером"

# from urllib.parse import urlencode

# params = {
#     "expand": "delivery,purchases,payment,status_payment",
#     "status": 1
# }

# prefix = f"orders/search?{urlencode(params)}"

class RozetMain(): 
    def __init__(self, token):
        self.bear_req = BearRequest()
        self.host = "https://api-seller.rozetka.com.ua/"
        self.cash = token # "Nj2HNztLCMG1pBnr18GtDZ-SSfj4-j5B"
        self.token_new = TokenRepServ()
        self.stub = Stub()

    def get_orders(self):
        status_load = self.stub.status_order_load()
        prefix = "orders/search?expand="
        prefix += "delivery,purchases,payment,status_payment"
        prefix += f"&status={status_load}"
        resp = self.make_request("GET", prefix)
        # print("dev_main_roz:", resp)
        if "content" in resp:
            if "orders" in resp["content"]:
                if resp["content"]["orders"]:
                    orders = []
                    for order in resp["content"]["orders"]:
                        ob_order = OrderRozetkaDTO.model_validate(order)
                        orders.append(ob_order)
                    return orders                  
        return None
    
    def mapper_status(self, status):
        statuses = {
            1: 26
        }
        if status in statuses:
            return statuses[status]
    
    def change_status(self, order_id, status):
        prefix = f"orders/{order_id}"
        body = {
            "status": self.mapper_status(status)
        }
        print("change_status:", body, prefix)
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
    
    def get_order_id(self): #черновик
        prefix = "orders/search?expand="
        prefix += "delivery,purchases,payment,status_payment"
        prefix += f"&page=1&sort=-id&type=2&id=841603966"
    
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
            # print("make_request12", headers)
        responce = self.request_go(method, url, headers, body)
        # print("Rozetka_make_request:", responce)
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

    # def make_order(self, data):
    #     delivery = data["delivery"]
    #     purchases = data["purchases"]
    #     payment = data["payment"]
    #     return {
    #         "id": data["id"],
    #         "event_date": data["created"],
    #         "user_phone": data["user_phone"],
    #         "client_firstname": data["user_title"]["first_name"],
    #         "client_lastname": data["user_title"]["last_name"],
    #         "client_surname": data["user_title"]["second_name"],
    #         "recipient_phone": data["recipient_phone"],
    #         "recipient_firstname": data["recipient_title"]["first_name"],
    #         "recipient_lastname": data["recipient_title"]["last_name"],
    #         "recipient_surname": data["recipient_title"]["second_name"],
    #         "another_recipient": False,
    #         "delivery_service_id": 
    #             self.delivery_service_id(delivery["delivery_service_id"]),
    #         "delivery_service_name": delivery["delivery_service_name"],
    #         "city_name": delivery["city"]["city_name"],
    #         "city_ref": delivery["city"]["uuid"],
    #         "region": delivery["city"]["region_title"],
    #         "delivery_method_id": delivery["delivery_method_id"],
    #         "place_street": delivery["place_street"],
    #         "place_number": delivery["place_number"],
    #         "place_house": delivery["place_house"],
    #         "place_flat": delivery["place_flat"],
    #         "warehouse_ref": delivery["ref_id"],
    #         "payment_option": payment["payment_method_name"],
    #         "payment_status": payment["payment_status"],
    #         "ordered_product": purchases,
    #         "amount": data["amount"],
    #         "sum_price": data["amount"],     
    #         "description": data["comment"],
    #         "description_delivery": data["user_title"],
    #         "cpa_commission": data["user_title"],
    #         "client_id": data["user_title"],
    #         "order_code": data["user_title"],
    #         "warehouse_method_id": data["user_title"],
    #         "source_order_id": data["user_title"],
    #         "payment_method_id": data["user_title"],
    #         "delivery_method_id": data["user_title"],
    #         "pickup_rz_id": data["delivery"]["pickup_rz_id"],
    #         "area":"",
    #         "client_notes": data["comment"]
    #     }
    
    def delivery_service_id(self, id):
        if id == 43660: # новапошта
            method = 1
        elif id == 4:
            method = 1
        elif id == 2024: # укрпошта
            method = 1
        elif id == 5: # новапошта
            method = 1
        elif id == 1:
            method = 1
        else:
            return 1
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
    
    def available_delivery(self):
        prefix = "orders/available-deliveries?sla_rz_id=0"
        resp = self.make_request("GET", prefix)
        print(resp)
        return resp
    
 
    

    
   



            
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

