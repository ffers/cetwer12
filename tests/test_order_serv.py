import os
from exceptions.order_exception import *

from server_flask.flask_app import flask_app
from server_flask.db import db
import requests, responses


from .lib.rozet_dict import RozetDict
from .lib.tg_lib import LibTG
from .lib.prom_dict import PromDict

from black.order_cntrl import OrderCntrl
from a_service.order_service.order_serv import OrderServ 

from api import RozetMain, EvoClient
from repository.store_sqlalchemy import StoreRepositorySQLAlchemy



class TestOrderServ: # пооки іде все через кнтрл
    order_c = OrderServ(store_repo=StoreRepositorySQLAlchemy(db.session))
    prom_token = os.getenv('PROM_TOKEN')
    rozet_token = os.getenv('ROZETKA_TOKEN')
    env = os.getenv("ENV")

    def status_dev(self):
        if self.env == "dev":
            return 5 
        else:
            return 1

    @responses.activate
    def test_get_order_rozet(self):
        with flask_app.app_context():
            host = "https://api-seller.rozetka.com.ua/"
            prefix = "orders/search" 
            # query = "expand="
            # query += "delivery,purchases,payment,status_payment"
            # query += f"&status={self.status_dev()}"
            responses.add(
                responses.GET, host+prefix,
                json=RozetDict.rozet_order, status=200,
                )
            self.make_response_tg()
            resp = self.order_c.load_orders_store_v2(
                "conus", self.rozet_token, EvoClient, RozetMain)
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
            host = "https://my.prom.ua/"
            prefix = "api/v1/orders/list?status=pending"
            responses.add(
                responses.GET, host+prefix,
                json=PromDict.orders, status=200
                )
            prefix2 = "api/v1/orders/list?status=paid"
            responses.add(
                responses.GET, host+prefix2,
                json={}, status=200
                )
            # self.make_response_tg()
            resp = self.order_c.load_orders_store_v2(
                "jemis", self.prom_token, EvoClient, RozetMain)
            print(resp)
            pointer = resp["result"].get('error')
            assert pointer == 'Замовлення вже існує'

    # @responses.activate
    # def test_get_unpay(self):
    #     try:
    #         with flask_app.app_context():
    #             self.make_response_tg()
    #             host = "https://my.prom.ua/"
    #             prefix = "api/v1/orders/33839071023"
    #             responses.add(
    #                 responses.GET, host+prefix,
    #                 json=PromDict.order, status=200
    #                 )
    #             pointer = self.order_c.get_status_unpay(
    #                 "vida", self.prom_token, EvoClient, RozetMain
    #                 )
    #             assert pointer == True
    #     except AllOrderPayException:
    #         assert True

