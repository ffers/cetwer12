from black import tg_cntrl
from helperkit import FileKit
from dotenv import load_dotenv
import os, json, requests

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
fl_cl = FileKit()

elements_to_remove = set()

payment_option_test = "../common_asx/payment_option_test.json"
unpay_order_file = "../common_asx/unpay_order.json"
canceled_order_file = "../common_asx/canceled_order.json"
data_order = "../common_asx/data.json"
url_update = 'http://localhost:8000/cabinet/orders/get_product/update_with_prom'

  #-421982888 /// -1001979021180 chat pidtverzgenya /// CHAT_ID_CONFIRMATION //// CHAT_ID_INFO
chat_id = os.getenv("CHAT_ID_CONFIRMATION")

class Changes:
    def search_canceled(self):
        data = fl_cl.load_file_json(canceled_order_file)
        canceled_order = set(data)
        print("Дивимось чи скасовано замовленя")
        data_all_order = fl_cl.load_file_json(data_order)
        for order in data_all_order["orders"]:
            if order["status"] == "canceled":
                if order["id"] not in canceled_order:
                    print("скасовані замовленя знайдені")
                    order_id = order["id"]
                    canceled_order.add(order_id)
                    order_list = list(canceled_order)
                    fl_cl.save_file_json(canceled_order_file, order_list)
                    tg_cntrl.sendMessage(chat_id, f"Скасовано {order_id}")
                    try:
                        self.send_http_json(order_id, "canceled") # відправляєм в базу данних
                    except:
                        tg_cntrl.sendMessage(chat_id, f"не вийшло додати в crm: Скасовано {order_id}")


    def writeOrderUnpay(self, file, order, processed_orders):
        order_id = order["id"]
        try:
            self.send_http_json(order_id, "unpaid")  # відправляєм в базу данних
        except:
            tg_cntrl.sendMessage(chat_id, f"не вийшло додати в crm: Скасовано {order_id}")
        processed_orders.add(order_id)
        list_order = list(processed_orders)
        fl_cl.save_file_json(file, list_order)

    def search_unpay(self):
        data_test = fl_cl.load_file_json(payment_option_test) # добавляю тестовий файл для сообщения о новом заказе промоплатой
        processed_test = set(data_test) # множество тестове
        data_unpay = fl_cl.load_file_json(unpay_order_file)
        processed_orders = set(data_unpay)
        print("Дивимось оплату")
        data = fl_cl.load_file_json(data_order)
        for order in data["orders"]:
            if order["payment_option"] != None:
                if order["payment_option"]["id"] == 7547964:
                    if order["id"] not in processed_orders:
                            if order["payment_data"] != None:
                                if order["id"] not in processed_test:  # якщо нема в тестовому бо буде слать всі замовленя
                                    # test_info = order["payment_data"] # ця частина для тесту
                                    # tg_cl.send_message_f(chat_id, f"Нове замовленя промоплатою {order_id}\n " # ця частина для тесту
                                    #                               f"Його payment_data: \n {test_info}") # ця частина для тесту
                                    print(f"ця частина для тесту") # ця частина для тесту
                                    self.writeOrderUnpay(payment_option_test, order, processed_test)  # ця частина для тесту
                                if order["payment_data"]["status"] == "unpaid":
                                    print("Найшли не сплачене")
                                    if order["id"] not in processed_orders:
                                        self.writeOrderUnpay(unpay_order_file, order, processed_orders)
                            else:
                                self.writeOrderUnpay(unpay_order_file, order, processed_orders)

    def search_pay(self):
        self.search_unpay()
        print("Дивимось чи змінився статус оплати")
        data_unpay = fl_cl.load_file_json(unpay_order_file)
        order_unpay = set(data_unpay)

        data = fl_cl.load_file_json(data_order)
        for order_data in data["orders"]:
            for order in order_unpay:
                if order == order_data["id"]:
                    if order_data["payment_data"]:
                        if order_data["payment_data"]["status"] == "paid":
                            print("Прийшла оплата")
                            tg_cntrl.sendMessage(chat_id, f"Оплачено {order}")
                            elements_to_remove.add(order)
                            self.send_http_json(order, "paid")
                            break

        if elements_to_remove:
            print(f"елементи для видалення {elements_to_remove}")
            new_order_unpay = order_unpay - elements_to_remove
            elements_to_remove.clear()
            list_order = list(new_order_unpay)
            fl_cl.save_file_json(unpay_order_file, list_order)
            print(new_order_unpay)

    def search_refunded(self, order_id):
        pass

    def send_http_json(self, order_id, flag):
        data = {"order_id": order_id, "flag": flag}
        json_data = json.dumps(data)
        token = os.getenv("SEND_TO_CRM_TOKEN")
        try:
            headers = {'Content-Type': 'application/json', "Authorization": token}
            resp = requests.post(url_update, data=json_data, headers=headers)
            print(resp.text)  # виведе відповідь від сервера
            return json.loads(resp.content)
        except:
            print("Сервер не відповідає")




