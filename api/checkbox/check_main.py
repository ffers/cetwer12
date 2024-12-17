import os, time, json, requests, uuid

import test
from utils import BearRequest
 
class CheckboxClient(object):
    def __init__(self, token=None):
        self.token = os.getenv("CHECKBOX_TOKEN")
        self.client_version = os.getenv('CHECKBOX_CLIENT_VERSION')
        self.license_key = os.getenv('CHECKBOX_LICENSE_KEY')
        self.device_id = os.getenv('DEVICE_ID')
        self.host = os.getenv('CHECKBOX_HOST')
        self.client_name = os.getenv("CHECKBOX_CLIENT_NAME")
        self.pin_cashier = os.getenv("CHECKBOX_PIN_CASHIER")
        self.token_veryfy = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiQVBJIiwianRpIjoiYjAwNmM0MTItOGFlYS00YjI1LTliMGMtNWRiM2M5NWE1ZGU5Iiwic3ViIjoiOGZiZDc0MWQtY2I2ZC00MDU0LThjMjctMGY5NjVlOGYxZWExIiwibmJmIjoxNzM0MjkyNzcyLCJpYXQiOjE3MzQyOTI3NzJ9.A3xZYY45STCoFDLSsM3jkHPumX1A0E4NraWcNw-EsW0"
        self.pin_cashier = os.getenv("CHECKBOX_PIN_CASHIER")


    def make_request(self, method, url, body=None):
        url = self.host + url
        headers = {
            "accept": "application/json",
            "X-Client-Name": "{}".format(self.client_name),
            "X-Client-Version": "{}".format(self.client_version),
            "X-License-Key": "{}".format(self.license_key),
            "X-Device-ID": "{}".format(self.device_id),
            "Content-type": "application/json"
        }
        print(headers)
        bear_req = BearRequest()
        responce = bear_req.request_go(method, url, headers, body)
        return responce

    def cash_registers(self):
        pass

    def signinPinCode(self):
        body = { "pin_code": self.pin_cashier }
        responce = self.make_request("POST", "api/v1/cashier/signinPinCode", body)
        token_auth = responce["access_token"]
        return responce
    
    def signout(self):
        responce = self.api.make_request("POST", "api/v1/cashier/signout")
        return responce


    



