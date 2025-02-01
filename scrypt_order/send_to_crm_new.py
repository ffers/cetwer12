from utils import BearRequest, UtilsAsx
from black import TelegramController
import os, json




class SendToCrmNew:
    def __init__(self):
        self.bear = BearRequest()
        self.log = UtilsAsx()
        self.set_log = self.log.oc_log("send_to_crm")

    def get_count_sold(self):
        url = "v2/analitic/count_sold"
        resp = self.milky_way("GET", url)
        print(resp, "відповідь")

    def get_orders_rozet(self):
        url = "v2/order/get_orders"
        resp = self.milky_way("GET", url)
        print(resp, "відповідь")

    def get_check(self):
        url = "v2/check/check_sign"
        resp = self.milky_way("GET", url)
        print(resp, "відповідь")

    def start_16_58(self):
        url = "v2/analitic/start_16_58"
        resp = self.milky_way("GET", url)
        print(resp, "відповідь")

    def start_17_00(self):
        url = "v2/analitic/start_17_00"
        resp = self.milky_way("GET", url)
        print(resp, "відповідь")

    def start_20_00(self):
        url = "v2/analitic/start_20_00"
        resp = self.milky_way("GET", url)
        print(resp, "відповідь")

    def start_20_01(self):
        url = "v2/analitic/start_20_01"
        resp = self.milky_way("GET", url)
        print(resp, "відповідь")
        
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
