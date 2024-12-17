from utils import BearRequest
# from common_asx.utilits import utils_dev_change

import os, base64
  

class RozetMain():
    def __init__(self):
        self.bear_req = BearRequest()
        self.host = "https://api-seller.rozetka.com.ua/"
        self.cash = False
        self.token = self.login()

    def get_orders(self):
        prefix = "orders/search-data"
        body = {
            "types": 2
        }
        resp = self.make_request("POST", prefix, body)
        return resp
    
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

    def make_request(self, method, prefix, body=None, headers=None):
        url = self.host + prefix
        if not headers:
            headers = {
                "Content-Type": "application/json", "Authorization": self.token
            }
        print(headers)
        responce = self.request_go(method, url, headers, body)
        return responce
    
    def request_go(self, method, url, headers, body):
        responce = self.bear_req.request_go(method, url, headers, body)
        print(method, url, headers, body, "проверка 1 ")
        if responce["success"] == False:
            self.cash = False
            self.token = self.login()
            if self.token:
                print(method, url, headers, body, "проверка")
                responce = self.bear_req.request_go(method, url, headers, body)
                return responce
            
    