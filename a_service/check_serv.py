from repository import UserTokenRep
from api import CheckboxClient
from DTO import UserTokenDTO
import uuid, time

        


class CheckServ(object):
    def __init__(self, user_id):
        from black import TelegramController
        self.tg = TelegramController()
        self.user_id = user_id
        self.token = None
        self.rep = UserTokenRep(None)
        self.authorization()
        self.api = CheckboxClient(self.token)


    def cash_register_operating(self):
        cash_online = self.cash_online_check()
        if cash_online:
            self.online_mode()
        if not cash_online:
            ping = self.try_online()
            if ping:
                cash_online = self.cash_online_check()
                if cash_online:
                    self.online_mode()
            else:
                self.offline_mode() 

    def online_mode(self):
        body = self.shifts_body()
        shifts_open = self.shifts_open(body)
        fiscal_code = self.load_offline_codes(True)
        shifts = self.online_mode()
        if shifts:
            next_step = None
        return shifts_open   
    
    def offline_mode(self):
        fiscal_code = None
        fiscal_date = None
        body = self.shifts_body(fiscal_code, fiscal_date)
        self.shifts_open(body)
                    
    def try_online(self, fiscal_code):
        ping = self.ping_tax_service()
        if ping == "DONE":
            go_online = self.go_online()
            if go_online:
                return True
    
    def shifts_open(self, body):
        try:
            shifts = self.api.shifts(body)
            times = 0
            while times <= 5:
                status = self.api.shifts_status(shifts["id"])
                if status.get["status"] == "OPENED":
                    return status
                time.sleep(2)
                times += 1
            else:
                raise Exception(f"Змінна не відкрилася {body}")     
        except Exception as e:
            self.tg.sendMessage(self.tg.chat_id_info, str(e))
            return None   
        
    def shifts_body(self, fiscal_code=None, fiscal_date=None):
        return {
            "id": str(uuid.uuid4()),
            "fiscal_code": fiscal_code,
            "fiscal_date": fiscal_date
            }
        
    def load_offline_codes(self, offline_mode):
        fiscal_code = self.get_offline_codes()
        if not offline_mode and fiscal_code < 500:
            self.ask_offline_codes() 
            fiscal_code = self.get_offline_codes()
            # может записать в базу
        return fiscal_code
    
    def cash_online_check(self):
        cash_id = None
        status = self.cash_online(cash_id)
        if status["offline_mode"]:
            return False
        return True
    
    def shifts(self, body):
        return self.universal_api_call(self.api.shifts(body))

    def go_online(self):
        return self.universal_api_call(self.api.go_online)

    def ask_offline_codes(self):
        return self.universal_api_call(self.api.ask_offline_codes)
    
    def get_offline_codes(self):
        return self.universal_api_call(self.api.get_offline_codes)

    def cash_registers(self):
        return self.universal_api_call(self.api.cash_registers)
    
    def cash_online(self, id):
        return self.universal_api_call(self.api.cash_online(id))
    
    def ping_tax_service(self):
        return self.universal_api_call(self.api.ping_tax_service)
    
    def add_token(self, token):
        self.token = token
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
    
    def validate_error(self, resp):
        
        if "error" in resp: # додати обробку різних помилок
                msg = ">>> {}".format(resp["error"])
                send = self.tg.sendMessage(tg.chat_id_info, msg)
                return True
        return False
        
    def validate_token(self):
        if not self.token:
            self.authorization()
            if not self.token:
                raise ValueError("Токен відсутній. Авторизуватись не вийшло. відправка в тг")
        self.api = CheckboxClient(self.token)

    def universal_api_call(self, func, *args, **kwargs):
        self.validate_token()
        try:
            resp = func(*args, **kwargs)
            success = self.validate_error(resp)
            if not success:
                return resp 
            raise
        except Exception as e:
            return False
            
    def authorization(self): # authorization
        print("Authorization Checkbox")
        self.token = self.rep.load_token_checkbox(self.user_id)
        if not self.token:
            api = CheckboxClient()
            success, resp = api.signinPinCode()
            if not success:
                self.validate_error(resp)
                print("Authorization unsuccessful")
                return False
            self.add_token(resp)
            print(f"Authorization success {resp}")
        return True