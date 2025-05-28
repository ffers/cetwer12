
import json, os
import responses

from fastapi.testclient import TestClient
from server_fast.app import app  

from .lib.tg_lib import LibTG
from .lib.prom_dict import PromDict

from exceptions.order_exception import *


client = TestClient(app)

@responses.activate
def test_read_main():
    with TestClient(app, base_url="http://localhost"):
            make_responce()
            make_response_tg()
            token_crm = os.getenv("SEND_TO_CRM_TOKEN")
            token_prom = os.getenv("PROM_TOKEN")
            # url = f"api_name=jemis"
            # url += f"&source_token={token_prom}"
            params = {
                'api_name': 'jemis',
                'store_token': token_prom
            }
            header = {
                    "Content-Type": "application/json", 
                    "Authorization": f"{token_crm}"
                }
            response = client.get(f"/v2/order/get_status_unpay", params=params, headers=header)
            cont = json.loads(response.content)
            print('cont:', cont)
            if cont['message'] == "all order paid":
                assert response.status_code == 200
            elif cont['message'] == "dont have change":
                assert response.status_code == 200
            else:
                assert cont == {"message":"have result"}
                assert response.status_code == 200
  

def make_responce():
    host = "https://my.prom.ua/"
    prefix = "api/v1/orders/342860627"
    responses.add(
        responses.GET, host+prefix,
        json=PromDict.order, status=200
        )

def make_response_tg():
    tg_token = os.getenv('TELEGRAM_BOT_TOKEN')
    host = f'https://api.telegram.org/bot{tg_token}/sendMessage'
    responses.add(
    responses.POST, host,
    json=LibTG.sendMessage, status=200
    )
    

    return True



