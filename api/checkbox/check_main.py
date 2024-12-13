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
        responce = bear_req.request(method, url, headers, body)
        return responce


    



