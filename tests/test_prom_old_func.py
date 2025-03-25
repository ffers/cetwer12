
from black.add_order_to_crm import PromToCrm

from server_flask.flask_app import flask_app
import requests, responses
from utils import Stub
from .lib.prom_dict import PromDict

class TestProm:
    lib = PromDict()
    prom = PromToCrm()


    def test_get_order(self):
        with flask_app.app_context():
            pointer = self.prom.add_order(self.lib.order, {"text":"text"})
            assert pointer == True

    # def make_response_tg(self):
    #     host = "https://api.telegram.org/bot603175634:AAHNHBKy56g37S1WiS1KZuw_a-aZjahqD7o/sendMessage"
    #     responses.add(
    #     responses.POST, host,
    #     json=TgLib.sendMessage, status=200
    #     )
    #     return True

