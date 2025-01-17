
import os, time, json, requests, uuid



class BearRequest:
    def request_go(self, method, url, headers, body=None):
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
                if response.status_code in [422, 403, 401]:
                    print("Код 422, 403 або 401")
                    return {"error":json.loads(response.content)}
                else:
                    print(f"Помилка: {e} - Відповідь сервера")
                    retries += 1 
                    print(f"Таймаут. Спроба {retries} з {max_retries}")
                    time.sleep(1)  # Зачекати перед наступною спробою
        else:
            print("Запит не вдалося виконати після {} спроб".format(max_retries))
            raise ValueError("Запит не вдалося виконати після {} спроб".format(max_retries))
        return json.loads(response.content)