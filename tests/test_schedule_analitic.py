




import json, os
import responses

from fastapi.testclient import TestClient
from server_fast.app import app  

from .lib.tg_lib import LibTG
from .lib.prom_dict import PromDict

from exceptions.order_exception import *


client = TestClient(app)

class TestScheduleAn:
    def test_start_16_58(self):
        url = "/v2/analitic/start_16_58"
        response, cont = self.milky_way(url)
        if cont['message'] == "all order paid":
            assert response.status_code == 200
        else:
            assert cont == {"message":"SUCCESS"}
            assert response.status_code == 200


    def test_start_17_00(self):
        url = "/v2/analitic/start_17_00"
        response, cont = self.milky_way(url)
        if cont['message'] == "all order paid":
            assert response.status_code == 200
        else:
            assert cont == {"message":"SUCCESS"}
            assert response.status_code == 200


    def test_start_20_00(self):
        url = "/v2/analitic/start_20_00"
        response, cont = self.milky_way(url)
        if cont['message'] == "all order paid":
            assert response.status_code == 200
        else:
            assert cont == {"message":"SUCCESS"}
            assert response.status_code == 200


    def test_start_20_01(self):
        url = "/v2/analitic/start_20_01"
        response, cont = self.milky_way(url)
        if cont['message'] == "all order paid":
            assert response.status_code == 200
        else:
            assert cont == {"message":"SUCCESS"}
            assert response.status_code == 200 

    def function_name(self):
        pass

    def make_response_tg(self):
        tg_token = os.getenv('TELEGRAM_BOT_TOKEN')
        host = f'https://api.telegram.org/bot{tg_token}/sendMessage'
        responses.add(
        responses.POST, host,
        json=LibTG.sendMessage, status=200
        )
        host2 = f'https://api.telegram.org/bot{tg_token}/sendPhoto'
        responses.add(
        responses.POST, host2,
        json=LibTG.sendMessage, status=200
        )
        return True
    

    def make_responce(self):
        self.make_response_tg()
        self.make_responce_np()
        host = "https://my.prom.ua/"
        prefix = "api/v1/orders/342394092"
        responses.add(
            responses.GET, host+prefix,
            json=PromDict.order, status=200
            )
        
    def make_responce_np(self):
        host = "https://api.novaposhta.ua/v2.0/json/"
        responses.add(
            responses.GET, host,
            json=LibTG.sendMessage, status=200
            )
        


    @responses.activate
    def milky_way(self, url, params=None):
        with TestClient(app, base_url="http://localhost"):
            self.make_responce()
            token_crm = os.getenv("SEND_TO_CRM_TOKEN")
            token_prom = os.getenv("PROM_TOKEN")
            header = {
                    "Content-Type": "application/json", 
                    "Authorization": f"{token_crm}"
                }
            response = client.get(url, params=params, headers=header)
            print(response.content)
            cont = json.loads(response.content)
            return response, cont