from utils import BearRequest
import os


class RozetMain(object):
    def __init__(self, token=None):
        self.bear_req = BearRequest()
        self.host = "https://api-seller.rozetka.com.ua/"

    def main(self):
        body = self.login()
        resp = self.make_request("POST", "sites", body)
        print(resp)
        return resp

    def login(self):
        username = os.getenv("rozet_username")
        password = os.getenv("rozet_password")
        body = {
            "username": username,
            "password": password
        }
        return body

    def make_request(self, method, prefix, body=None):
        url = self.host + prefix
        headers = {
            "Content-Type": "application/json"
        }
        print(headers)
        responce = self.bear_req.request_go(method, url, headers, body)
        return responce