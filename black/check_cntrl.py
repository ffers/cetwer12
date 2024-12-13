import os

from api import CheckboxClient
from a_service import TokenRepServ

class CheckCntrl:
    def __init__(self):
        self.token = os.getenv("CHECKBOX_TOKEN")
        self.api = CheckboxClient(self.token)
        self.pin_cashier = os.getenv("CHECKBOX_PIN_CASHIER")

    def signinPinCode(self, responce):
        body = { "pin_code": self.pin_cashier }
        # responce = self.api.make_request("POST", "api/v1/cashier/signinPinCode", body)
        print(f"відповідь сервера {responce}")
        token_auth = responce["access_token"]
        return responce

    def signout(self):
        responce = self.api.make_request("POST", "api/v1/cashier/signout")
        return responce
    
    def test_crypto(self):
        token_rep_serv = TokenRepServ()
        token_rep_serv.test_token_crypt()
        return True
    





