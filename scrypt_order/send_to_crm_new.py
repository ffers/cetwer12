from utils import BearRequest, OC_logger
from black import TelegramController
import os, json




class SendToCrmNew:
    def __init__(self):
        self.bear = BearRequest()
        self.log = OC_logger
        self.set_log = self.log.oc_log("send_to_crm")

    def get_count_sold(self):
        url = "v2/analitic/count_sold"
        resp = self.milky_way("GET", url)


    def get_orders(self, api_name, token):
        url = f"v2/order/get_orders?api_name={api_name}&store_token={token}"
        resp = self.milky_way("GET", url)


    def get_check(self):
        url = "v2/check/check_sign"
        resp = self.milky_way("GET", url)


    def start_16_58(self):
        url = "v2/analitic/start_16_58"
        resp = self.milky_way("GET", url)


    def start_17_00(self):
        url = "v2/analitic/start_17_00"
        resp = self.milky_way("GET", url)


    def start_20_00(self):
        url = "v2/analitic/start_20_00"
        resp = self.milky_way("GET", url)


    def start_20_01(self):
        url = "v2/analitic/start_20_01"
        resp = self.milky_way("GET", url) 

        
    def milky_way(self, method, prefix):
        url = os.getenv("HOSTCRM") + prefix
        token = os.getenv("SEND_TO_CRM_TOKEN")
        header = {
                "Content-Type": "application/json", 
                "Authorization": f"{token}"
            }
        return self.send_request(method, url, header)

    def send_request(self, method, url, header):
        self.tg = TelegramController()
        try:
            resp = self.bear.request_go(method, url, header)
            return resp
        except Exception as e:
            self.tg.sendMessage(self.tg.chat_id_info, 
                                f"🔴 🔴 🔴  Сервер не працює! \n {e}")
            return False
