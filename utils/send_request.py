import os, json, requests

class SendRequest:
    def __init__(self) -> None:
        self.token = os.getenv("SEND_TO_CRM_TOKEN")

    def send_http_json(self, data, url):
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json', "Authorization": self.token}
        # try:
        resp_json = requests.post(url, data=json_data, headers=headers, timeout=5)
        resp = json.loads(resp_json.content)
        print(resp)
        return resp
        # except:
        #     print("Сервер не отвечаєт")
        #     return False