
from api.nova_poshta import create_ttn_button
from api import EvoClient, RozetMain
from api.nova_poshta.create_data import RegistrDoc
from api.nova_poshta.create_data import ListClient
from api.nova_poshta import CreateNpData
from repository import OrderRep
from dotenv import load_dotenv
from .delivery_order_cntrl import DeliveryOrderCntrl
from .telegram_controller import tg_cntrl

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
from server_flask.db import db
import sys,os

sys.path.append('../')
from common_asx.utilits import Utils


ttn_ref_list = "../common_asx/ttn_ref_list.json"

AUTH_TOKEN = os.getenv("PROM_TOKEN")
evo_cl = EvoClient(AUTH_TOKEN)
ls_cl = ListClient()
reg_cl = RegistrDoc()
crnp_cl = CreateNpData()
# cab_cl = NpCabinetCl()
ut_cl = Utils(EvoClient, RozetMain)
ord_rep = OrderRep()
del_ord_cntrl = DeliveryOrderCntrl()

chat_id_info = os.getenv("CHAT_ID_INFO")


RESP = {}

dict_ttn_prom = {
              "order_id": "",
              "declaration_id": "",
              "delivery_type": "nova_poshta"
            }

dict_status_prom = {
          "ids": [ 0 ],
          "custom_status_id":  137639
        }

class ManagerTTN:

    def create_ttn(self, order):
        order_id = order["id"]
        try:
            ttn_data = create_ttn_button(order)
            if ttn_data["success"] == False:
                tg_cntrl.sendMessage(chat_id_info,
                            f"Замовленя {order_id}, не створенно!\n {ttn_data}")
            else:
                ttn_data = self.manipulation_tnn(order_id, ttn_data)
                return ttn_data
        except:
            exep_text = f"❗️❗️❗️ Замовлення {order_id} не створено НП"
            print(exep_text)
            tg_cntrl.sendMessage(chat_id_info, exep_text)

    def manipulation_tnn(self, order_id, ttn_data):
        ref = reg_cl.create_ref(ttn_data)
        ls_cl.add_in_list(ttn_ref_list, ref)
        ttn = ttn_data["data"][0]["IntDocNumber"]
        resp_true = self.add_ttn_crm(order_id, ttn_data)
        order = crnp_cl.order_send()
        text = self.create_text(ttn_data, order)
        delivery_type = "nova_poshta"
        resp_prom = self.update_prom_order(ttn, order_id, delivery_type)
        if resp_prom == "Пром не відповідає":
            tg_cntrl.sendMessage(chat_id_info, f"❗️❗️❗️ Створено 🥊{text} АЛЕ {resp_prom}!")
        else:
            tg_cntrl.sendMessage(chat_id_info,
                                 f"🥊 Створено - {text}🥊 ТТН додано!")
        print(ttn)
        return ttn_data

    def make_send_ttn(self, ttn, order_id, delivery_type=None):
        if delivery_type:
            dict_ttn_prom.update({"order_id": order_id, "declaration_id": ttn, "delivery_type": delivery_type})
        else:
            dict_ttn_prom.update({"order_id": order_id, "declaration_id": ttn})
        print(dict_ttn_prom)
        global RESP
        RESP.update(ut_cl.change_ttn(dict_ttn_prom))
        print(RESP)
        return RESP

    def make_set_status(self, ttn, order_id):
        dict_status_prom.update({"ids": [order_id]})
        error = None
        if "error" == RESP["status"]:
            if RESP["errors"] != None:
                error = RESP["errors"]
            if RESP["message"] != None:
                error = RESP["message"]
            tg_cntrl.sendMessage(chat_id_info, f"Помилка валідації по замовленю {order_id}, ttn: {ttn}, помилка {error}")
            # evo_cl.get_set_status(dict_status_prom)
        else:
            status = ut_cl.change_status(dict_status_prom)
            return status

    def all_product(self, order):
        all_products = []
        for sku in order["products"]:
            product = {
                "artikul": sku["sku"],
                "name_multilang": sku["name_multilang"]["uk"],
                "price": sku["price"],
                "quantity": sku["quantity"],
                "measure_unit": sku["measure_unit"],
                "image_url": sku["image"],
                "total_price": sku["total_price"]
            }
            all_products.append(product)
        text = ""
        for product in all_products:
            text += f"{product['artikul']} - {product['quantity']} {product['measure_unit']} - {product['price']} \n"
        return text

    def create_text(self, ttn_data, order):
        order_id = order["id"]
        docNumber = ttn_data["data"][0]["IntDocNumber"]
        SUN = crnp_cl.sun_send()
        phone = SUN["RecipientsPhone"]
        warehouse_n = SUN["warehouse_n"]
        CityName = SUN["CityName"]
        text = f" {order_id}\n {CityName}: №{warehouse_n}\n{phone};{docNumber}\n"
        return text



    def update_prom_order(self, ttn, order_id, delivery_type):
        resp = "Пром не відповідає"
        try:
            resp = self.make_send_ttn(ttn, order_id, delivery_type)
            resp = self.make_set_status(ttn, order_id)
            return resp
        except:
            return resp


    def add_ttn_crm(self, order_id, ttn_data):
        try:
            ttn = ttn_data["data"][0]["IntDocNumber"]
            ttn_ref = ttn_data["data"][0]["Ref"]
            order = ord_rep.load_for_code(order_id)
            order.ttn = ttn
            order.ttn_ref = ttn_ref
            order.ordered_status_id = 2
            db.session.commit()
            self.add_del_ord(ttn_data, order.id)
            print("ттн додано до CRM")
            return True
        except Exception as e:
            print(f"В срм не додано {e}")
            return False

    def add_del_ord(self, first_data, order_id):
        print("add_del_ord")
        del_ord_cntrl.update_item(first_data, order_id)
        return True
