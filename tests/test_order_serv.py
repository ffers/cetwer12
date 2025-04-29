from black.tg_answer_cntrl import OrderCntrl
from .lib.rozet_dict import RozetDict
from .lib.tg_lib import LibTG
from .lib.prom_dict import PromDict
from server_flask.flask_app import flask_app
import requests, responses
from utils import Stub
import os
from exceptions.order_exception import *

class TestOrderServ: # пооки іде все через кнтрл
    order_c = OrderCntrl()
    prom_token = os.getenv('PROM_TOKEN')
    rozet_token = os.getenv('ROZETKA_TOKEN')

    @responses.activate
    def test_get_order_rozet(self):
        with flask_app.app_context():
            self.stub = Stub()
            host = "https://api-seller.rozetka.com.ua/"
            status_load = self.stub.status_order_load()
            prefix = "orders/search?expand="
            prefix += "delivery,purchases,payment,status_payment"
            prefix += f"&status={status_load}"
            responses.add(
                responses.GET, host+prefix,
                json=RozetDict.rozet_order, status=200
                )
            # self.make_response_tg()
            resp = self.order_c.load_orders_store("rozetka", self.rozet_token)
            print(resp)
            pointer = resp["result"].get('error')
            assert pointer == 'Замовлення вже існує'

    def make_response_tg(self):
        tg_token = os.getenv('TELEGRAM_BOT_TOKEN')
        host = f'https://api.telegram.org/bot{tg_token}/sendMessage'
        responses.add(
        responses.POST, host,
        json=LibTG.sendMessage, status=200
        )
        return True
    
    @responses.activate
    def test_get_order_prom(self):
        with flask_app.app_context():
            self.make_response_tg()
            self.stub = Stub()
            host = "https://my.prom.ua/"
            status_load = self.stub.status_order_load()
            prefix = "/api/v1/orders/list?status=pending"
            responses.add(
                responses.GET, host+prefix,
                json=PromDict.order_prom_2, status=200
                )
            # self.make_response_tg()
            resp = self.order_c.load_orders_store("prom", self.prom_token)
            print(resp)
            pointer = resp["result"].get('error')
            assert pointer == 'Замовлення вже існує'

    @responses.activate
    def test_get_unpay(self):
        try:
            with flask_app.app_context():
                self.make_response_tg()
                self.stub = Stub()
                host = "https://my.prom.ua/"
                status_load = self.stub.status_order_load()
                prefix = "api/v1/orders/341112473"
                responses.add(
                    responses.GET, host+prefix,
                    json=PromDict.order_prom_2, status=200
                    )
                # self.make_response_tg()
                pointer = self.order_c.status_payment_search_times("prom", self.prom_token)
                assert pointer == True
        except AllOrderPayException:
            assert True

