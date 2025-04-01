import os, json, requests, time
from os.path import join, dirname
from requests.exceptions import ReadTimeout
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from .time_now import time_now

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)

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

class NpClient(object):
    def __init__(self, token=None):
        self.token = os.getenv("NP_TOKEN")
        self.CitySender = os.getenv("NP_CITY_SENDER")
        self.Sender = os.getenv("NP_SENDER_REFLS")
        self.SenderAddress = os.getenv("NP_SENDER_ADRESS")
        self.CityRecipient = os.getenv("NP_CITY_SENDER")
        self.ContactSender = os.getenv("NP_COUNT_REFLS")
        self.pas_token = token


    def try_resp(self, data, flag=None):
        try:
            json_data = json.dumps(data)
            resp = self._request_np(json_data)
            print(resp)
            if flag == "Ref":
                if "Ref" in resp["data"][0]:
                    resp = resp["data"][0]["Ref"]
                else:
                    resp = print(f"Помилка реф не отримано {resp}")
                return resp
        except:
            resp = print("Не получилось получить ответ")
        return resp

    def date_today_np(self):
        date_time = time_now()
        next_time = next(date_time)
        time_for_np = next_time.strftime("%d.%m.%Y")
        return time_for_np


    def json_read_dict(self, file):
        with open(file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def read_data_order(self, file):
        with open(file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def get_from_env(self, key):
        dotenv_path = join(dirname(__file__), '../.env')
        load_dotenv(dotenv_path)
        print()
        return os.environ.get(key)

    def _request_np(self, updated_json):
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

    def runup_doc(self, sun):
        data = {
            "apiKey": self.token,
            "modelName": "InternetDocument",
            "calledMethod": "save",
            "methodProperties": {
                "SenderWarehouseIndex": "38/17",
                "RecipientWarehouseIndex": "",
                "PayerType": "Recipient",
                "PaymentMethod": "Cash",
                "DateTime": self.date_today_np(),
                "CargoType": "Parcel",
                "VolumeGeneral": "0.0004",
                "Weight": "0.5",
                "ServiceType": "WarehouseWarehouse",
                "SeatsAmount": "1",
                "Description": sun["Description"],
                "Cost": sun["Cost"],
                "CitySender": self.CitySender,
                "Sender": self.Sender,
                "SenderAddress": self.SenderAddress,
                "ContactSender": self.ContactSender,
                "SendersPhone": "380989323122",
                "CityRecipient": sun["CityRecipient"],
                "Recipient": sun["Recipient"],
                "RecipientAddress": sun["RecipientAddress"],
                "ContactRecipient": sun["ContactRecipient"],
                "RecipientsPhone": sun["RecipientsPhone"]
            }}
        if "AfterpaymentOnGoodsCost" in sun:
            data["methodProperties"]["AfterpaymentOnGoodsCost"] = sun["AfterpaymentOnGoodsCost"]
        if "OptionsSeat" in sun:
            data["methodProperties"]["OptionsSeat"] = sun["OptionsSeat"]
        resp = self.try_resp(data)
        return resp

    def getWarehouses_str(self, description=None, TypeOfWarehouseRef=None):
        print(description)
        data = {
            "apiKey": self.token,
            "modelName": "Address",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "FindByString": description,
                "TypeOfWarehouseRef": TypeOfWarehouseRef
            }
        }
        json_data = json.dumps(data)
        resp = self._request_np(json_data)
        return resp

    def getSettlementCountryRegion(self, AreaRef):
        data = {
           "apiKey": self.token,
           "modelName": "Address",
           "calledMethod": "getSettlementCountryRegion",
           "methodProperties": {
                "AreaRef" : AreaRef
           }
        }
        json_data = json.dumps(data)
        resp = self._request_np(json_data)
        return resp

    def insertDocumentsReg(self, data_ref):
        data = {
            "apiKey": self.token,
            "modelName": "ScanSheet",
            "calledMethod": "insertDocuments",
            "methodProperties": {
                "DocumentRefs": data_ref
            }
        }
        json_data = json.dumps(data)
        resp = self._request_np(json_data)
        return resp

    def addDocumentsReg(self, data_ref, reg_ref):
        data = {
            "apiKey": self.token,
            "modelName": "ScanSheet",
            "calledMethod": "insertDocuments",
            "methodProperties": {
                "DocumentRefs": data_ref,
                "Ref": reg_ref
            }
        }
        resp = self.try_resp(data)
        return resp

    def removeDocumentsReg(self, data_ref, reg_ref):
        data = {
            "apiKey": self.token,
            "modelName": "ScanSheet",
            "calledMethod": "removeDocuments",
            "methodProperties": {
                "DocumentRefs": data_ref,
                "Ref": reg_ref
            }
        }
        resp = self.try_resp(data)
        return resp

    def deleteScanSheet(self, reg_ref):
        data = {
               "apiKey": self.token,
               "modelName": "ScanSheet",
               "calledMethod": "deleteScanSheet",
               "methodProperties": {
            "ScanSheetRefs" : reg_ref
           }
        }
        resp = self.try_resp(data)
        return resp

    def create_contragent(self, sun):
        data = {
            "apiKey": self.token,
            "modelName": "Counterparty",
            "calledMethod": "save",
            "methodProperties": {
                "FirstName": sun["FirstName"],
                "MiddleName": sun.get("MiddleName", ""),
                "LastName": sun["LastName"],
                "Phone": sun["RecipientsPhone"],
                "Email": "test@i.com",
                "CounterpartyType": "PrivatePerson",
                "CounterpartyProperty": "Recipient"
            }}
        ref = self.try_resp(data, "Ref")
        return ref

    def create_contact(self, details):
        data = {
            "apiKey": self.token,
            "modelName": "ContactPerson",
            "calledMethod": "save",
            "methodProperties": {
                "CounterpartyRef": details["Recipient"],
                "FirstName": details["FirstName"],
                "LastName": details["LastName"],
                "MiddleName": details["MiddleName"],
                "Phone": details["RecipientsPhone"]
            }}
        ref = self.try_resp(data, "Ref")
        return ref

    def get_search_warhouse(self, buffer):
        data = {
            "apiKey": self.token,
            "modelName": "Address",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "CityName": buffer["CityName"],
                "CityRef": buffer["CityRef"],
                "Page": "1",
                "Limit": "50",
                "Language": "UA",
                "TypeOfWarehouseRef": buffer["TypeOfWarehouseRef"],
                "WarehouseId": buffer["WarehouseId"],
                "FindByString": buffer["FindByString"]
            }}
        resp = self.try_resp(data)
        return resp

    def get_s_war_ref(self, ref):
        data = {
            "apiKey": self.token,
            "modelName": "Address",
            "calledMethod": "getWarehouses",
            "methodProperties": {
                "Ref": ref
            }}
        resp = self.try_resp(data)
        return resp



    def trackingDocument(self, list_ref):
        data = {
            "apiKey": self.token,
            "modelName": "TrackingDocument",
            "calledMethod": "getStatusDocuments",
            "methodProperties": {"Documents": list_ref}
                }
        resp = self.try_resp(data)
        return resp






