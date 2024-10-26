import os

from api import CheckboxClient


class CHECK_CNTRL():
    def __init__(self):
        self.token = os.getenv("CHECKBOX_TOKEN")
        self.api = CheckboxClient(self.token)
        self.pin_cashier = os.getenv("CHECKBOX_PIN_CASHIER")

    def signinPinCode(self):
        body = { "pin_code": self.pin_cashier }
        responce = self.api.make_request("POST", "api/v1/cashier/signinPinCode", body)
        print(f"відповідь сервера {responce}")
        token_auth = responce["access_token"]
        return responce

    def signout(self):
        responce = self.api.make_request("POST", "api/v1/cashier/signout")
        return responce



