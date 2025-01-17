from utils import BearRequest, UtilsAsx
from black import TelegramController
import os, json




class SendToCrmNew:
    def __init__(self):
        self.bear = BearRequest()
        self.log = UtilsAsx()
        self.set_log = self.log.oc_log("send_to_crm")

    def get_orders_rozet(self):
        host = os.getenv("HOSTCRM")
        url = host + "v2/order/get_orders"
        token = os.getenv("SEND_TO_CRM_TOKEN")
        header = {
                "Content-Type": "application/json", "Authorization": f"{token}"
            }
        resp = self.send_request("GET", url, header)
        print(resp, "відповідь")

    def get_check(self):
        host = os.getenv("HOSTCRM")
        url = host + "v2/check/check_sign"
        token = os.getenv("SEND_TO_CRM_TOKEN")
        header = {
                "Content-Type": "application/json", "Authorization": f"{token}"
            }
        resp = self.send_request("GET", url, header)
        print(resp, "відповідь")
        

    def send_request(self, method, url, header):
        self.tg = TelegramController()
        try:
            resp = self.bear.request_go(method, url, header)
            return resp
        except Exception as e:
            self.tg.sendMessage(self.tg.chat_id_info, f"🔴 🔴 🔴  Сервер не працює! \n {e}")
            return False
