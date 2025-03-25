from DTO import UserTokenDTO
from repository import UserTokenRep
from api import CheckboxClient



class Authorization:
    def __init__(self, user_id, Telegram):
        self.tg = Telegram()
        self.user_id = user_id
        self.token = None
        self.rep = UserTokenRep(None)
        self.client = CheckboxClient
        self.check_token()
        self.connect = False

    def check_token(self): # authorization
        print("Authorization Checkbox")
        self.token = self.rep.load_token_checkbox(self.user_id)
        print("authorization_func", self.token)
        if not self.token:
            return self.auth_get()
        self.connect = True
        return self.auth_check()
    
    def auth_get(self):
        api = self.client()
        success, resp = api.signinPinCode()
        if not success:
            self.validate_error(resp)
            print("Authorization unsuccessful")
            return False
        self.add_token(resp)
        print(f"Authorization success {resp}")
        return resp
    
        '''можливо якщо токен не працює треба переподключитися'''
    def auth_check(self):
        return self.token
    
    def add_token(self, token):
        self.token = token
        self.connect = True
        resp = self.rep.load_token_checkbox(self.user_id)
        dto = UserTokenDTO(
            user_id=self.user_id,
            checkbox_access_token=token
        ) 
        if not resp:
            print("Додаєм нового юзера")
            success = self.rep.add_token(dto)
            return success
        print("Оновлюємо данні юзера", dto)
        success = self.rep.update_token(dto)
        print("db:", success)
        return success