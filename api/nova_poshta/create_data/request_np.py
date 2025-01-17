import os, json, requests, time
from os.path import join, dirname
from requests.exceptions import ReadTimeout
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta


current_datetime = datetime.now(timezone.utc) + timedelta(hours=4)
date_today = current_datetime.strftime("%d.%m.%Y")
date_yesterday_nf = current_datetime - timedelta(days=7)
date_yesterday = date_yesterday_nf.strftime("%d.%m.%Y")
date_7day_nf = current_datetime - timedelta(days=1)
date_7day = date_7day_nf.strftime("%d.%m.%Y")
api_url = "https://api.novaposhta.ua/v2.0/json/"
filename = current_datetime.strftime("%Y-%m-%d_%H%M%S")
ttn_json_f_n = "api/nova_poshta/create_data/dovidka/dov_" + filename + ".json"
stat_json_f_n = filename + "st.json"
folder_path = "api/nova_poshta/create_data/dovidka"
files = os.listdir(folder_path)


def date_today_np():
    while True:
        current_datetime = datetime.now(timezone.utc) + timedelta(hours=4)
        date_today = current_datetime.strftime("%d.%m.%Y")
        yield date_today
        print(f"Текущее время: {date_today}")
        time.sleep(1)  # Обновлять время каждую секунду

date_today = date_today_np()

def json_read_dict(file):
    with open(file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def read_data_order(file):
    with open(file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def get_from_env(key):
    dotenv_path = join(dirname(__file__), '../common_asx/.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)

def request_np(updated_json):
    time.sleep(1)
    max_retries = 5  # Максимальна кількість спроб
    retries = 0
    timeout = 10
    response = None
    while retries < max_retries: 
        try:
            response = requests.get(api_url, data=updated_json, timeout=timeout)
            response.raise_for_status()
            break  # Завершити цикл, якщо запит успішний
        except ReadTimeout:
            retries += 1
            print(f"Таймаут. Спроба {retries} з {max_retries}")
        except requests.exceptions.RequestException as e:
            print(f"Помилка: {e}")
            break  # Вийти з циклу, якщо сталася помилка
    if response.status_code == 200:
        api_data = response.json()
        return api_data
    else:
        print("Помилка при відправці запиту. Статус код:", response.status_code)

def get_request_adress(json_data):
    data = json.loads(json_data)
    data["apiKey"] = get_from_env("NP_TOKEN")
    data["methodProperties"]["CounterpartyRef"] = get_from_env("NP_SENDER_REF")
    data["methodProperties"]["StreetRef"] = get_from_env("NP_SENDER_REF")
    json_data = json.dumps(data)
    resp = request_np(json_data)
    with open(ttn_json_f_n, 'w', encoding='utf-8') as file:
        # for item in responce:
            json.dump(resp, file, indent=4, ensure_ascii=False)
    return resp

def get_request_city(json_data):
    data = json_data["data"]["data_city"]
    data["apiKey"] = get_from_env("NP_TOKEN")
    data["methodProperties"]["FindByString"] = "Харків"
    json_data = json.dumps(data)
    resp = request_np(json_data)
    with open(ttn_json_f_n, 'w', encoding='utf-8') as file:
        # for item in responce:
            json.dump(resp, file, indent=4, ensure_ascii=False)
    return resp

def get_create_contragent(data, buffer):
    buffer = json.loads(buffer)
    data = data["data"]["Recepient"]
    data["apiKey"] = get_from_env("NP_TOKEN")
    data["methodProperties"]["FirstName"] = buffer["FirstName"]
    data["methodProperties"]["LastName"] = buffer["LastName"]
    data["methodProperties"]["MiddleName"] = buffer["MiddleName"]
    data["methodProperties"]["Phone"] = buffer["Phone"]
    print(data)
    json_data = json.dumps(data, ensure_ascii=False)
    resp = request_np(json_data)
    print(resp)
    Recipient = resp["data"][0]["Ref"]
    return Recipient

def get_create_contact(data, buffer):
    buffer = json.loads(buffer)
    data = data["data"]["ContactPerson"]
    data["apiKey"] = get_from_env("NP_TOKEN")
    data["methodProperties"]["CounterpartyRef"] = buffer["CounterpartyRef"]
    data["methodProperties"]["FirstName"] = buffer["FirstName"]
    data["methodProperties"]["LastName"] = buffer["LastName"]
    data["methodProperties"]["MiddleName"] = buffer["MiddleName"]
    data["methodProperties"]["Phone"] = buffer["RecipientsPhone"]
    json_data = json.dumps(data)
    resp = request_np(json_data)
    return resp

def get_search_contragent(data, buffer):
    buffer = json.loads(buffer)
    data = data["data"]["getCounterparties"]
    data["apiKey"] = get_from_env("NP_TOKEN")
    data["methodProperties"]["Page"] = buffer["Page"]
    json_data = json.dumps(data)
    resp = request_np(json_data)
    return resp

def get_search_contact(data, buffer):
    data = data["data"]["Counterparty"]
    data["apiKey"] = get_from_env("NP_TOKEN")
    data["methodProperties"]["Ref"] = buffer["Recipient"]
    data["methodProperties"]["Page"] = buffer["Page"]
    json_data = json.dumps(data)
    resp = request_np(json_data)
    print(f"Перевіряємо контакти {resp}")
    return resp

def get_search_warhouse(buffer):
    data = {
        "apiKey": get_from_env("NP_TOKEN"),
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "CityName": buffer["CityName"],
            "CityRef": buffer["CityRef"],
            "Page": buffer["Page"],
            "Limit": "100",
            "Language": "UA",
            "TypeOfWarehouseRef": buffer["TypeOfWarehouseRef"],
            "WarehouseId": buffer["WarehouseId"],
            "FindByString": buffer["FindByString"]
        }}

    json_data = json.dumps(data)
    resp = request_np(json_data)
    return resp



def searchSettlements(city):
    data = {
        "apiKey": get_from_env("NP_TOKEN"),
        "modelName": "Address",
        "calledMethod": "searchSettlements",
        "methodProperties": {
            "CityName": city
        }
    }
    json_data = json.dumps(data)
    resp = request_np(json_data)
    return resp

def getSettlements_Str(city):
    data = {
        "apiKey": get_from_env("NP_TOKEN"),
        "modelName": "Address",
        "calledMethod": "getSettlements",
        "methodProperties": {
            "FindByString": city
        }
    }
    json_data = json.dumps(data)
    resp = request_np(json_data)
    return resp

def get_Setlements(City, Area=None):
    data = {
       "apiKey": get_from_env("NP_TOKEN"),
       "modelName": "Address",
       "calledMethod": "searchSettlements",
       "methodProperties": {
            "AreaRef" : Area,
            "FindByString" : City
               }
            }
    json_data = json.dumps(data)
    resp = request_np(json_data)
    return resp

def get_generate_doc(data, sun):
    data = data["data"]["data_IntDocNumber"]
    data["apiKey"] = get_from_env("NP_TOKEN")
    data["methodProperties"]["DateTime"] = sun["DateTime"]
    data["methodProperties"]["Cost"] = sun["Cost"]
    data["methodProperties"]["CitySender"] = get_from_env("NP_CITY_SENDER")
    data["methodProperties"]["Sender"] = get_from_env("NP_SENDER_REFLS")
    data["methodProperties"]["SenderAddress"] = get_from_env("NP_SENDER_ADRESS")
    data["methodProperties"]["CityRecipient"] = get_from_env("NP_CITY_SENDER")
    data["methodProperties"]["ContactSender"] = get_from_env("NP_COUNT_REFLS")
    data["methodProperties"]["Recipient"] = sun["Recipient"]
    data["methodProperties"]["RecipientAddress"] = sun["RecipientAddress"]
    data["methodProperties"]["ContactRecipient"] = sun["ContactRecipient"]
    data["methodProperties"]["RecipientsPhone"] = sun["RecipientsPhone"]
    if sun["BackwardDeliveryData"] != None:
        data["methodProperties"]["AfterpaymentOnGoodsCost"] = sun["BackwardDeliveryData"][0]["RedeliveryString"]
    if sun["OptionsSeat"] != None:
        data["methodProperties"]["OptionsSeat"] = sun["OptionsSeat"]
    print(data)
    json_data = json.dumps(data)
    resp = request_np(json_data)
    return resp

