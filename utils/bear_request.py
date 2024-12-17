
import os, time, json, requests, uuid




class BearRequest:
    def request_go(self, method, url, headers, body):
        if body:
            body = json.dumps(body) 
        time.sleep(1)
        max_retries = 5  # Максимальна кількість спроб
        retries = 0
        timeout = 10
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