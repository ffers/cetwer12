
import os, time, json, requests, uuid
from utils import OC_logger


class BearRequest:
    logger = OC_logger.oc_log('utils.bear_request')

    def request_go(self, method, url, headers, body=None):
        if body:
            body = json.dumps(body) 
        time.sleep(1)
        max_retries = 5  # Максимальна кількість спроб
        retries = 0
        timeout = 20
        while retries < max_retries:
            try:
                response = requests.request(method, url, data=body, headers=headers, timeout=timeout)
                if response.status_code in [422, 403, 401]:
                    print("Код 422, 403 або 401")
                    return {"error":json.loads(response.content)}
                response.raise_for_status()  # Підняти виключення, якщо код статусу не 200
                print(f"Responce server: OK")
                break
            except requests.exceptions.RequestException as e:
                self.logger.error(f'{e}')
                print(f"Помилка: {e} - Відповідь сервера")
                retries += 1 
                print(f"Таймаут. Спроба {retries} з {max_retries}")
                time.sleep(1)  # Зачекати перед наступною спробою
            except Exception as e:
                self.logger.error(f'Непередбачувана помилка {e}')
        else:
            print("Запит не вдалося виконати після {} спроб".format(max_retries))
            raise ValueError("Запит не вдалося виконати після {} спроб".format(max_retries))
        return json.loads(response.content)