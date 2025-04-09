import os, json, requests, logging, pytz, time
from requests.exceptions import ReadTimeout
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
import http.client

'''
Щоб скасувати замовлення через API Prom.ua, 
необхідно передати параметр `cancellation_reason` 
із одним із наступних значень:

- `not_available`
- `price_changed`
- `buyers_request`
- `not_enough_fields`
- `duplicate`
- `invalid_phone_number`
- `less_than_minimal_price`
- `another`

Якщо обрано `price_changed`, `not_enough_fields` або `another`,
 потрібно додатково передати параметр `cancellation_text`
   з поясненням причини скасування. citeturn0search9 
'''

logging.basicConfig(filename='../common_asx/log_prom_api.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
georgia_timezone = pytz.timezone('Asia/Tbilisi')
current_time_georgia = datetime.now(georgia_timezone)

RESP = None
HOST = 'https://my.prom.ua'
chat_id = "-421982888"

print(f"Працює request...  {current_time_georgia}")

dict_ttn_prom = {
              "order_id": "",
              "declaration_id": "",
              "delivery_type": "nova_poshta"
            }

dict_status_prom = {
          "ids": [ 0 ],
          "custom_status_id":  137639
        }

def get_from_env(key):
    dotenv_path = join(dirname(__file__), '../common_asx/.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)

class HTTPError(Exception):
    pass

class EvoClient(object):

    def __init__(self, token):
        self.token = token

    def make_request(self, method, url, body=None):
        url = HOST + url
        print("make_request:", body)
        headers = {'Authorization': 'Bearer {}'.format(self.token),
                   'Content-type': 'application/json'}
        if body:
            body = json.dumps(body)
        time.sleep(1)
        max_retries = 5  # Максимальна кількість спроб
        retries = 0
        timeout = 10
        while retries < max_retries:
            try:
                response = requests.request(method, url, data=body, headers=headers, timeout=timeout)
                print(f"Відповідь пром {response}")
                response.raise_for_status()  # Підняти виключення, якщо код статусу не 200
                break
            except requests.exceptions.RequestException as e:
                print(f"Помилка: {e}")
                retries += 1
                print(f"Таймаут. Спроба {retries} з {max_retries}")
                time.sleep(1)  # Зачекати перед наступною спробою
        else:
            raise ValueError("Запит не вдалося виконати після {} спроб".format(max_retries))

        response_data = response.content
        
        return json.loads(response_data)

    def get_order_list(self, value_url=None):
        url = '/api/v1/orders/list'
        if value_url:
            url = f'/api/v1/orders/list{value_url}'
        method = 'GET'
        try:
            result = self.make_request(method, url)
            return result
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 500:
                print("Отримано помилку 500: Internal Server Error")
                # Тут ви можете виконати дії для обробки помилки 500
            else:
                print(f"Отримано HTTPError з кодом {e.response.status_code}")
                # Інші дії для обробки інших помилок
        except requests.exceptions.RequestException as e:
            print(current_time_georgia.strftime("%Y-%m-%d %H:%M:%S"),   f"Виникла помилка під час виконання запиту: {e}")
        except:
            return None
  

    def get_order_id(self, order_id):
        url = '/api/v1/orders/{id}'
        method = 'GET'
        return self.make_request(method, url.format(id=order_id))
    
    def get_orders(self):
        orders = []
        statuses = ("pending", "paid")
        for status in statuses:
            orders.extend(self.load_orders(status))
        return orders


    
    def load_orders(self, status): # треба переробити на різні статуси
        url = f'/api/v1/orders/list?status={status}'
        method = 'GET'
        data = self.make_request(method, url)
        return data.get("orders", [])

    def send_ttn(self, order_id, ttn, delivery_type):
        body = {
            "order_id": order_id,
            "declaration_id": ttn,
            "delivery_type": delivery_type
        }
        url = '/api/v1/delivery/save_declaration_id'
        method = 'POST'
        resp = self.make_request(method, url, body)
        print("change_status:", resp)
        return resp
    
    def create_body_status(self, order_id, status_order):
        dict_status_prom = None
        print(status_order)
        if 5 == status_order: # скасовано
            dict_status_prom = {
                "status": "canceled",
                "ids": [order_id],
                "cancellation_reason": "not_available",
                "cancellation_text": "Скасовано"
            }
        if 3 == status_order: # Дубль
            dict_status_prom = {
                "status": "canceled",
                "ids": [order_id],
                "cancellation_reason": "duplicate",
                "cancellation_text": "Дубль замовлення"
            }
        if 1 == status_order: # прийнято
            dict_status_prom = {
                "status": "received",
                "ids": [order_id]
            }
        if 2 == status_order: # підтверженно
            dict_status_prom = {
                "custom_status_id": 137639,
                "ids": [order_id]
            }
        return dict_status_prom

    def change_status(self, order_id, status):
        body = self.create_body_status(order_id, status)
        url = '/api/v1/orders/set_status'
        method = 'POST'
        resp = self.make_request(method, url, body)
        
        return resp
        

    def make_send_ttn(self, ttn, order_id, delivery_type=None):
        body = {
            "order_id": order_id,
            "declaration_id": ttn,
            "delivery_type": delivery_type
        }
        print(dict_ttn_prom)
        global RESP
        RESP = self.get_send_ttn(dict_ttn_prom)
        print(RESP)
        return RESP

    def send_message_f(self, chat_id, text, keyboard_json=None):
        method = "sendMessage"
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        url = f"https://api.telegram.org/bot{token}/{method}"
        if keyboard_json:
            data = {"chat_id": chat_id, "text": text, 'parse_mode': 'Markdown', "reply_markup":keyboard_json}
        else:
            data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)

    def make_set_status(self, ttn, order_id):
        dict_status_prom.update({"ids": [order_id]})
        if RESP["status"] == "error":
            error = RESP["errors"]
            self.send_message_f(chat_id, f"Помилка валідації по замовленю {order_id}, ttn: {ttn}, помилка {error}")
            self.get_set_status(dict_status_prom)
        else:
            self.send_message_f(chat_id, f"Валідація успішна по замовленю {order_id}, ttn: {ttn}")
            status = self.get_set_status(dict_status_prom)
            self.send_message_f(chat_id, f"Відповідь по зміні статусу {order_id} : {status}")
            return status


prom_api = EvoClient(get_from_env("PROM_TOKEN"))












