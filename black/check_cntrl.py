import os

from api import CheckboxClient


class CheckCntrl:
    def __init__(self):
        self.token = os.getenv("CHECKBOX_TOKEN")
        self.api = CheckboxClient(self.token)
        
    def signinPinCode(self):
        responce = self.api.signinPinCode()
        print(f"відповідь сервера {responce}")
        token_auth = responce["access_token"]
        return responce
    
    





