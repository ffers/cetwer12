from black import OrderCntrl
from a_service.order_service.order_serv import OrderServ
from server_flask.flask_app import flask_app
import requests, responses
from utils import Stub

from dataclasses import dataclass

@dataclass
class DataClient:
    id: int = 111
    client_firstname: str = "Тест"
    client_lastname: str = "Тест"
    client_surname: str = "Тестович"
    phone: str = "380333333333"
    email: str = "test@i.com"


class TestOrederCntrl:
    o_c = OrderCntrl()
    o_s = OrderServ() 
  
    def test_change_client(self):
        with flask_app.app_context():
            order = DataClient()
            print(order)
            order_list = [order]
            print(order_list)
            # order_list = self.o_c.load_all_order()
            result = self.o_s.change_order(order_list)
            assert result == True

    def test_load_order_new(self):
        with flask_app.app_context():
            result = self.o_c.load_status_id(10)
            assert isinstance(result, list)