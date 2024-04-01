import os, re, logging
from api.nova_poshta.create_data import NpClient
from server_flask.db import db
from server_flask.models import Orders, OrderedProduct, Products, TelegramOrdered, ConfirmedAddressTg
from flask import current_app
from telegram import TgClient
from dotenv import load_dotenv
from scrypt_order.current_changes_order import Changes

log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log_handler = logging.FileHandler("../common_asx/log/order_to_crm.log")
log_handler.setFormatter(log_formatter)

LOG = logging.getLogger("ord_to_crm")
LOG.setLevel(logging.INFO)
LOG.addHandler(log_handler)

ch_cl = Changes()
tg_cl = TgClient()
env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
chat_id_info = os.getenv("CHAT_ID_INFO")
chat_id_helper = os.getenv("CHAT_ID_HELPER")

class PromToCrm():
    def __init__(self):
        pass

    def add_order(self, json_order, data_for_tg):
        try:
            LOG.info(f"НАЧАЛОСЬ {json_order}")
            order = self.parse_order(json_order)
            order_id = order.id
            product = self.parse_product(json_order, order)
            self.add_ordered_telegram(data_for_tg, order_id)
            db.session.close()
            LOG.info(f"ЗАКІНЧИЛОСЬ {order}")
            return order_id
        except Exception as e:
            order_id = json_order["id"]
            LOG.info(f"Спрацював exept {e}")
            tg_cl.send_message_f(chat_id_helper, f"️❗️❗️❗️ НЕ ВИЙШЛО ДОДАТИ замовлення {order_id} В CRM сторона CRM")

    def parse_order(self, order):
        prompay_status_id = self.add_prompay_status(order)
        payment_method_id = self.add_payment_method_id(order)
        dict_parse = {
            "order_id_sources": order["id"],
            "description": self.add_description(order),
            "delivery_method_id": self.add_delivery_method(order),
            "CityRef": None,
            "CityName": None,
            "TypeWarehouse": None,
            "WarehouseText": order["delivery_address"],
            "phone": self.add_phone(order),
            "warehouse_method": None,
            "WarehouseRef": None,
            "payment_method_id": payment_method_id,
            "sum_before_goods": self.add_sum_before_goods(order, payment_method_id),
            "prompay_status_id": prompay_status_id,
            "ordered_status_id": self.add_order_status(prompay_status_id),
            "full_price": self.format_float(order["full_price"]),

        }
        dict_parse.update(self.add_address_dict_np(order, dict_parse))
        order = self.prepare_for_db(order, dict_parse)
        dict_parse.clear()
        return order

    def prepare_for_db(self, order, dict_parse):
        LOG.info(dict_parse)
        new_order = Orders(
            order_id_sources=str(order["id"]),
            description=dict_parse["description"],
            city_name=dict_parse["CityName"],
            city_ref=dict_parse["CityRef"],
            warehouse_text=dict_parse['WarehouseText'],
            warehouse_ref=dict_parse["WarehouseRef"],
            phone=dict_parse['phone'],
            client_firstname=order['client_first_name'],
            client_lastname=order['client_last_name'],
            client_surname=order['client_second_name'],
            warehouse_method_id=dict_parse['warehouse_method'],
            delivery_method_id=dict_parse["delivery_method_id"],
            payment_method_id=dict_parse["payment_method_id"],
            ordered_status_id=dict_parse["ordered_status_id"],
            prompay_status_id=dict_parse["prompay_status_id"],
            sum_price=dict_parse["full_price"],
            sum_before_goods=dict_parse["sum_before_goods"],
            cpa_commission=order["cpa_commission"]["amount"],
            client_id=order["client_id"],
            source_order_id=2,
            author_id=55
            )
        db.session.add(new_order)
        db.session.commit()
        return new_order

    def add_address_dict_np(self, order, dict_parse):
        if dict_parse["delivery_method_id"] == 1:
            try:
                data_address = self.get_data_address_np(order)
                dict_parse.update(self.create_address_dict_np(data_address))
                dict_parse.update(self.add_warehouse_method(dict_parse))
            except:
                order_id = order["id"]
                tg_cl.send_message_f(chat_id_helper, f"️❗️❗️❗️ Замовлення додано але адреси нема в № {order_id} ")
        return dict_parse


    def add_description(self, order):
        if order["client_notes"]:
            description = order["client_notes"]
            return description
        else:
            description = "Нотаток нема"
            return description

    def add_delivery_method(self, order):
        delivery_method_id = None
        delivery_method = order["delivery_option"]["id"]
        if delivery_method == 13013934:
            delivery_method_id = 1
        if delivery_method == 15255183:
            delivery_method_id = 2
        if delivery_method == 13844336:
            delivery_method_id = 3
        if delivery_method == 14383961:
            delivery_method_id = 4
        if delivery_method == 13013935:
            delivery_method_id = 5
        return delivery_method_id

    def get_data_address_np(self, order):
        token = os.getenv("NP_TOKEN")
        np_cl = NpClient(token)
        war_ref = order["delivery_provider_data"]["recipient_warehouse_id"]
        if not war_ref:
            raise
        data_address_draft = np_cl.get_s_war_ref(war_ref)
        data_address = data_address_draft["data"][0]
        return data_address

    def create_address_dict_np(self, data_address):
        address_dict_np = {
            "CityRef": data_address["CityRef"],
            "TypeWarehouse": data_address["TypeOfWarehouse"],
            "CityName": data_address["CityDescription"],
            "WarehouseText": data_address["Description"],
            "WarehouseRef": data_address["Ref"]
        }
        return address_dict_np

    def add_phone(self, order):
        draft_phone = order['phone']
        item_filter = re.findall(r'\d{12}', draft_phone)
        phone = item_filter[0]
        return phone

    def add_payment_method_id(self, order):
        payment_method_id = None
        payment_option = order["payment_option"]["id"]
        if payment_option in (9289897, 8362873):
            payment_method_id = 1
        if payment_option in (9289898, 7111681):
            payment_method_id = 2
        if payment_option == 7495540:
            payment_method_id = 3
        if payment_option == 8281881:
            payment_method_id = 4
        if payment_option == 7547964:
            payment_method_id = 5
        return payment_method_id

    def add_prompay_status(self, order):
        status_id = None
        payment_option = order["payment_option"]["id"]
        if payment_option == 7547964:
            payment_data = order["payment_data"]
            LOG.info(payment_data)
            if payment_data != None:
                if "paid" == payment_data["status"]:
                    status_id = 1
                elif "refunded" == payment_data["status"]:
                    status_id = 3
                else:
                    status_id = 2
                LOG.info(status_id)
                return status_id
            else:
                status_id = 2
        return status_id

    def add_order_status(self, prompay_status_id):
        LOG.info(f"Статус промоплати {prompay_status_id}")
        status_order = 10
        if prompay_status_id == 1:
            status_order = 3
        elif prompay_status_id == 2:
            status_order = 4
        elif prompay_status_id == 3:
            status_order = 4
        return status_order

    def add_sum_before_goods(self, order, payment_method_id):
        sum_before_goods = None
        if payment_method_id == 3:
            sum_before_goods = self.format_float("100")
        return sum_before_goods

    def add_warehouse_method(self, address_dict):
        if address_dict["TypeWarehouse"] == "f9316480-5f2d-425d-bc2c-ac7cd29decf0":
            dict_warehouse = {"warehouse_method": 2}
        else:
            dict_warehouse = {"warehouse_method": 1}
        return dict_warehouse

    def parse_product(self, order, object_order):
        for product in order["products"]:
            product_id = self.check_product(product)
            price = self.format_float(product["price"])
            product_order = OrderedProduct(product_id=product_id, price=price, quantity=product["quantity"],
                                     order_id=object_order.id)
            db.session.add(product_order)
        db.session.commit()

    def check_product(self, product):
        with current_app.app_context():
            search = Products.query.filter_by(article=product["sku"]).first()
            if search:
                return search.id
            else:
                product_id = self.create_product(product)
                return product_id

    def create_product(self, product):
        with current_app.app_context():
            create = Products(
                article=product["sku"],
                product_name=product["name_multilang"]["uk"],
                price=self.format_float(product["price"]),
                quantity=product["quantity"])
            db.session.add(create)
            db.session.commit()
            product_in_db = Products.query.filter_by(article=product["sku"]).first()
            return product_in_db.id

    def format_float(self, num_str_text):
        try:
            num_str = ''.join(re.findall(r'\b\d+[.,]?\d*\b', num_str_text))
            if "," in num_str:
                num_str = num_str.replace(',', '.')
            num = float(num_str)
            # Якщо число - ціле, додаємо ".00"
            if num.is_integer():
                num_dr = f"{int(num)}.00"
                return float(num_dr)
            else:
                return float(num)
        except ValueError:
            return "Неправильний формат числа"

    def add_ordered_telegram(self, data_for_tg, order_id):
        LOG.info(f"data_for_tg {data_for_tg}")
        tg_ord = TelegramOrdered(
            text=data_for_tg["text"],
            order_id=order_id)
        db.session.add(tg_ord)
        db.session.commit()
        conf_addr_tg = ConfirmedAddressTg(
            message_id=data_for_tg["message_id"],
            chat_id=data_for_tg["chat_id"],
            tg_ord_id=tg_ord.id
        )
        db.session.add(conf_addr_tg)
        db.session.commit()
        LOG.info("НАЧЕ ДОДАНО")