from black import OrderCntrl
from server_flask.flask_app import flask_app
import requests, responses
from utils import Stub


class TestOrederCntrl:
    o_c = OrderCntrl()

    # def test_change_client(self):
    #     with flask_app.app_context():
    #         result = self.o_c.update_client_info()
    #         assert result == True

    def test_load_order_new(self):
        with flask_app.app_context():
            result = self.o_c.load_status_id(10)
            assert isinstance(result, list)