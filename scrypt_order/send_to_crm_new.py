from utils import BearRequest, OC_logger
from a_service import TgServNew
import os, json




class SendToCrmNew:
    def __init__(self):
        self.bear = BearRequest()
        self.logger = OC_logger.oc_log("scrypt.send_to_crm_new")

    def get_count_sold(self):
        url = "v2/analitic/count_sold"
        resp = self.make_request("GET", url)


    def get_orders(self, api_name, token):
        url = f"v2/order/get_orders?"
        url += f"api_name={api_name}"
        url += f"&store_token={token}"
        # url += f"&store_name={name}"
        resp = self.make_request("GET", url)

        ''' Короткий вариант
        стор нейм как определить
        подписать стор 
        и использовать етот нейм в тексте
        '''
        '''
        таблица сторов
        добавить стор нейм, апі_токен, обрати маркет
        при завантаженні по токену знайти ці данні 
        та завантажити и прописати все необхідне
        '''

    def get_status_unpay(self, api_name, token):
        try:
            url = f"v2/order/get_status_unpay?"
            url += f"api_name={api_name}"
            url += f"&store_token={token}"
            # url += f"&store_name={name}"
            resp = self.make_request("GET", url)
        except Exception as e:
            self.logger.error(f'{e}')

    def get_check(self):
        url = "v2/check/check_sign"
        resp = self.make_request("GET", url)


    def start_16_58(self):
        url = "v2/analitic/start_16_58"
        resp = self.make_request("GET", url)

    def close_group(self):
        url = "v2/analitic/close_group"
        resp = self.make_request("GET", url)


    def start_17_00(self):
        url = "v2/analitic/start_17_00"
        resp = self.make_request("GET", url)


    def start_20_00(self):
        url = "v2/analitic/start_20_00"
        resp = self.make_request("GET", url)


    def start_20_01(self):
        url = "v2/analitic/start_20_01"
        resp = self.make_request("GET", url) 

    
    def update_analitic(self):
        url = "v2/analitic/update_analitic"
        return self.make_request("GET", url) 
    
    def report(self):
        url = "v2/analitic/report"
        return self.make_request("GET", url) 
    
    def diff_count_sold(self):
        url = "v2/analitic/diff_count_sold"
        return self.make_request("GET", url) 

        
    def make_request(self, method, prefix):
        url = os.getenv("HOSTCRM") + prefix
        token = os.getenv("SEND_TO_CRM_TOKEN")
        header = {
                "Content-Type": "application/json", 
                "Authorization": f"{token}"
            }
        return self.send_request(method, url, header)

    def send_request(self, method, url, header):
        self.tg = TgServNew()
        try:
            resp = self.bear.request_go(method, url, header)
            if 'error' in resp:
                error = str(resp['error'])
                print(error)
                self.logger.error(error)
                raise ValueError(error)
            if 'message' in resp:
                message = str(resp['message'])
                print(message)
                self.logger.info(message)
            return resp
        except Exception as e:
            self.tg.sendMessage(self.tg.chat_id_info, 
                                f"🔴 🔴 🔴  Сервер не працює! \n {e}")
            return False
