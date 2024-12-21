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
                return resp
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
        # print(headers)
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