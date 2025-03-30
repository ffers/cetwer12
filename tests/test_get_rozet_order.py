from black.tg_answer_cntrl import OrderCntrl
from .lib.rozet_dict import RozetDict
from .lib.tg_lib import TgLib
from server_flask.flask_app import flask_app
import requests, responses
from utils import Stub

class TestRozet:
    order_c = OrderCntrl()

    @responses.activate
    def test_get_order(self):
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
            self.make_response_tg()
            pointer = self.order_c.load_orders_store("rozetka")
            print(pointer)
            assert pointer == True

    def make_response_tg(self):
        host = "https://api.telegram.org/bot603175634:AAHNHBKy56g37S1WiS1KZuw_a-aZjahqD7o/sendMessage"
        responses.add(
        responses.POST, host,
        json=TgLib.sendMessage, status=200
        )
        return True

