
import os, time, json, requests, uuid
from utils import OC_logger


class BearRequest:
    logger = OC_logger.oc_log('utils.bear_request')

    def request_go(self, method, url, headers, body=None):
        if body:
            body = json.dumps(body) 
        time.sleep(1)
        max_retries = 3  # Максимальна кількість спроб
        retries = 0
        timeout = 10
        while retries < max_retries:
            try:
                response = requests.request(method, url, data=body, headers=headers, timeout=timeout)
                if response.status_code in [422, 403, 401]:
                    self.logger.info("Код 422, 403 або 401")
                    return {"error":json.loads(response.content)}
                response.raise_for_status()  # Підняти виключення, якщо код статусу не 200
                self.logger.info(f"Responce server: OK")
                break
            except requests.exceptions.Timeout:
                self.logger.error("Хтось не відповідає — таймаут") # змінити "хтось" на url
            except requests.exceptions.RequestException as e:
                self.logger.error(f'{e}')
                self.logger.info(f"Помилка: {e} - Відповідь сервера")
                retries += 1 
                self.logger.info(f"Таймаут. Спроба {retries} з {max_retries}")
                time.sleep(1)  # Зачекати перед наступною спробою
            except Exception as e:
                self.logger.error(f'Непередбачувана помилка {e}')
        else:
            self.logger.error("Запит не вдалося виконати після {} спроб".format(max_retries))
            raise ValueError("Запит не вдалося виконати після {} спроб".format(max_retries))
        return json.loads(response.content)

    