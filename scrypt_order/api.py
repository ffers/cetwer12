import json, os, requests

url_update = 'http://localhost:8000/cabinet/orders/get_product/update_with_prom'

def send_http_json(self, order_id, flag):
    data = {"order_id": order_id, "flag": flag}
    json_data = json.dumps(data)
    token = os.getenv("SEND_TO_CRM")
    try:
        headers = {'Content-Type': 'application/json', "Authorization": token}
        resp = requests.post(url_update, data=json_data, headers=headers)
        print(resp.text)  # виведе відповідь від сервера
        return json.loads(resp.content)
    except:
        print("Сервер не відповідає")