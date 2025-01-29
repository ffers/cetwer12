import os, time, json, requests, uuid
from pydantic import AliasGenerator, BaseModel, ConfigDict
from typing import List, Optional
from utils import BearRequest

class HeadersModel(BaseModel):  
    accept: str = "application/json"
    X_Client_Name: str = os.getenv("CHECKBOX_CLIENT_NAME")
    X_Client_Version: str = os.getenv('CHECKBOX_CLIENT_VERSION')
    X_License_Key: Optional[str] = None
    X_Device_ID: Optional[str] = None
    Authorization: Optional[str] = None
    Content_Type: str = None
        
    model_config = ConfigDict(
        alias_generator = AliasGenerator(
       serialization_alias = lambda field_name: field_name.replace("_", "-")
        )
    )
 
class CheckboxClient(object):
    def __init__(self, token=None):
        self.token = os.getenv("CHECKBOX_TOKEN")
        self.license_key = os.getenv('CHECKBOX_LICENSE_KEY')
        self.device_id = os.getenv('DEVICE_ID')
        self.host = os.getenv('CHECKBOX_HOST')
        self.pin_cashier = os.getenv("CHECKBOX_PIN_CASHIER")
        self.token_veryfy = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiQVBJIiwianRpIjoiYjAwNmM0MTItOGFlYS00YjI1LTliMGMtNWRiM2M5NWE1ZGU5Iiwic3ViIjoiOGZiZDc0MWQtY2I2ZC00MDU0LThjMjctMGY5NjVlOGYxZWExIiwibmJmIjoxNzM0MjkyNzcyLCJpYXQiOjE3MzQyOTI3NzJ9.A3xZYY45STCoFDLSsM3jkHPumX1A0E4NraWcNw-EsW0"
        self.pin_cashier = os.getenv("CHECKBOX_PIN_CASHIER")
        self.cash = token

    def receipts_status(self, id): 
        prefix = f"receipts/sell/{id}"
        obj = HeadersModel(
            X_License_Key=self.license_key,
            Authorization=f"Bearer {self.cash}",
            Content_Type="application/json"
        )
        headers = obj.model_dump(by_alias=True)
        responce = self.request_go("GET", prefix, headers)
        return responce

    def receipts_sell(self, body):
        prefix = "receipts/sell"
        obj = HeadersModel(
            X_License_Key=self.license_key,
            Authorization=f"Bearer {self.cash}",
            Content_Type="application/json"
        )
        headers = obj.model_dump(by_alias=True)
        responce = self.request_go("POST", prefix, headers, body)
        return responce
    
    def shift_status(self, id):
        prefix = f"shifts/{id}"
        obj = HeadersModel(
            X_License_Key=self.license_key,
            Authorization=f"Bearer {self.cash}"
        )
        headers = obj.model_dump(by_alias=True)
        responce = self.request_go("GET", prefix, headers)
        return responce

    #Якщо каса не перейшла у онлайн - варто відправити /api/v1/cash-registers/go-online ще раз та знову перевірити через хвилину статус каси, повторюючи дії в циклі, поки каса не вийде у онлайн-режим.
    def shifts(self, body):
        prefix = "shifts"
        obj = HeadersModel(
            X_License_Key=self.license_key,
            Authorization=f"Bearer {self.cash}",
            Content_Type="application/json"
        )
        headers = obj.model_dump(by_alias=True)
        responce = self.request_go("POST", prefix, headers, body)
        return responce

    def go_online(self):
        prefix = "cash-registers/go-online"
        obj = HeadersModel(
            X_License_Key=self.license_key,
            Authorization=f"Bearer {self.cash}"
        )
        headers = obj.model_dump(by_alias=True)
        responce = self.request_go("POST", prefix, headers)
        return responce
    
    def go_offline(self):
        prefix = "cash-registers/go-offline"
        obj = HeadersModel(
            X_License_Key=self.license_key,
            Authorization=f"Bearer {self.cash}"
        )
        headers = obj.model_dump(by_alias=True)
        responce = self.request_go("POST", prefix, headers)
        return responce
    
    def ask_offline_codes(self):
        prefix = "cash-registers/ask-offline-codes"
        obj = HeadersModel(
            X_License_Key=self.license_key,
            Authorization=f"Bearer {self.cash}"
        )
        headers = obj.model_dump(by_alias=True)
        responce = self.request_go("GET", prefix, headers)
        return responce
        
    def get_offline_codes(self):
        prefix = "cash-registers/get-offline-codes"
        obj = HeadersModel(
            X_License_Key=self.license_key,
            Authorization=f"Bearer {self.cash}"
        )
        headers = obj.model_dump(by_alias=True)
        responce = self.request_go("GET", prefix, headers)
        return responce

    def cash_registers(self):
        prefix = f"cash-registers/info"
        obj = HeadersModel(
            X_License_Key=self.license_key
        )
        headers = obj.model_dump(by_alias=True)
        responce = self.request_go("GET", prefix, headers)
        return responce
    
    def cash_online(self, id): 
        prefix = f"cash-registers/7671f8df-8b98-4860-83c6-918e5001fad0"
        obj = HeadersModel(
            Authorization=f"Bearer {self.cash}"
        )
        headers = obj.model_dump(by_alias=True)
        responce = self.request_go("GET", prefix, headers)
        return responce
       
    def ping_tax_service(self):
        prefix = f"cash-registers/ping-tax-service"
        obj = HeadersModel(
            X_License_Key=self.license_key,
            Authorization=f"Bearer {self.cash}"
        )
        headers = obj.model_dump(by_alias=True)
        responce = self.request_go("POST", prefix, headers)
        return responce
    
    def signinPinCode(self): 
        obj = HeadersModel(
            Content_Type="application/json",
            X_License_Key=self.license_key
        )
        headers = obj.model_dump(by_alias=True)
        prefix = "cashier/signinPinCode"
        body = { "pin_code": self.pin_cashier }
        responce = self.request_go("POST", prefix, headers, body)
        if "access_token" in responce:
            return True, responce["access_token"]
        else:
            return False, responce["detail"]
    
    # def signout(self):
    #     responce = self.api.make_request("POST", "api/v1/cashier/signout")
    #     return responce

    def request_go(self, method, prefix, headers, body=None):
        url = self.host + prefix
        bear_req = BearRequest()
        print(method, url, headers, body)
        responce = bear_req.request_go(method, url, headers, body)
        return responce

    



