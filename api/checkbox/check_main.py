import os, time, json, requests, uuid

class CheckboxClient(object):
    def __init__(self, token=None):
        self.token = os.getenv("CHECKBOX_TOKEN")
        self.client_version = os.getenv('CHECKBOX_CLIENT_VERSION')
        self.license_key = os.getenv('CHECKBOX_LICENSE_KEY')
        self.device_id = os.getenv('DEVICE_ID')
        self.host = os.getenv('CHECKBOX_HOST')
        self.client_name = os.getenv("CHECKBOX_CLIENT_NAME")
        self.pin_cashier = os.getenv("CHECKBOX_PIN_CASHIER")

    def make_request(self, method, url, body=None):
        url = self.host + url
        headers = {
            "accept": "application/json",
            "X-Client-Name": "{}".format(self.client_name),
            "X-Client-Version": "{}".format(self.client_version),
            "X-License-Key ": "{}".format(self.license_key),
            "X-Device-ID": "{}".format(self.device_id),
            "Content-type": "application/json"
        }
        print(headers)
        responce = self._request(method, url, headers, body)
        return responce

    def _request(self, method, url, headers, body):
        if body:
            body = json.dumps(body)
        time.sleep(1)
        max_retries = 5  # Максимальна кількість спроб
        retries = 0
        timeout = 10
        print(body)
        print(url)
        print(headers)
        while retries < max_retries:
            try:
                response = requests.request(method, url, data=body, headers=headers, timeout=timeout)
                print(f"Відповідь сервера {json.loads(response.content)}")
                response.raise_for_status()  # Підняти виключення, якщо код статусу не 200
                break
            except requests.exceptions.RequestException as e:
                print(f"Помилка: {e} - Відповідь сервера {json.loads(response.content)}")
                retries += 1
                print(f"Таймаут. Спроба {retries} з {max_retries}")
                time.sleep(1)  # Зачекати перед наступною спробою
        else:
            print("Запит не вдалося виконати після {} спроб".format(max_retries))
            raise ValueError("Запит не вдалося виконати після {} спроб".format(max_retries))

        response_data = response.content
        return json.loads(response_data)
