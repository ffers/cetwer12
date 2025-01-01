import os
# from server_flask.flask_app import flask_app
from api import CheckboxClient


class CheckCntrl:
    def __init__(self):
        self.token = os.getenv("CHECKBOX_TOKEN")
        # with flask_app.app_context:
        self.api = CheckboxClient(self.token)
        
    def signinPinCode(self):
        responce = self.api.signinPinCode()
        token_auth = responce["access_token"]
        return responce 
    
    





