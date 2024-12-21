from utils import BearRequest, UtilsAsx
from black import TelegramController
import os, json




class SendToCrm:
    def __init__(self):
        self.bear = BearRequest()
        self.log = UtilsAsx()
        self.set_log = self.log.oc_log("send_to_crm")

    def make_request(self):
        url = "https://localhost:8000/v2/admin/market_get_orders"
        token = os.getenv("SEND_TO_CRM_TOKEN")
        header = {
                "Content-Type": "application/json", "Authorization": f"Bearer {token}"
            }
        resp = self.bear("POST", url, header)

    def send_request(self, url, header):
        try:
            resp_json = self.bear("POST", url, header)
            resp = json.loads(resp_json.content)
            if not resp:
                self.tg = TelegramController()
                self.tg.sendMessage(self.tg.chat_id_info, f"Сервер не відповідає на пошук замовленнь")
            return resp
        except:
            print("send_request_new не працює")
            return False