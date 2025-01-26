import uuid, time, datetime
from repository import UserTokenRep
from api import CheckboxClient
from DTO import UserTokenDTO, ReceiptDTO, ShiftDTO
from repository import ReceiptRep, ShiftRep
 
class CheckServ(object):
    def __init__(self, user_id):
        from black import TelegramController 
        self.tg = TelegramController()
        self.user_id = user_id
        self.token = None
        self.token_rep = UserTokenRep(None)
        self.authorization()
        self.api = CheckboxClient(self.token)
        self.receipt_rep = ReceiptRep()
        self.shift_rep = ShiftRep()

    def cash_register_operating(self):
        cash_online = self.cash_online_check()
        if cash_online:
            online = self.online_mode()
            if online:
                pass
        if not cash_online:
            ping = self.try_online()
            if ping:
                cash_online = self.cash_online_check()
                if cash_online:
                    self.online_mode()
            else:
                self.offline_mode() 

    def online_mode(self):
        fiscal_code = self.load_offline_codes(True)
        shifts = self.load_shift()
        if shifts:
            pass
            # чекі
        else:
            return False
    
    def offline_mode(self):
        offline = self.go_offline()
        if offline.get("status") == "ok":
            shift = self.load_shift()
            if shift:
                pass
                # чекі
            else:
                fiscal_code = None
                fiscal_date = None
                body = self.shifts_body(fiscal_code, fiscal_date)

            self.shifts_open(body)
                    
    def try_online(self, fiscal_code):
        ping = self.ping_tax_service()
        if ping == "DONE":
            return True
        else: 
            return False
        
    def load_shift(self):
        load_shift = self.shift_rep.load_shift_today(datetime.datetime.utcnow())
        if load_shift:
            return load_shift
        else:
            body = self.shifts_body()
            shift = self.shift_open(body)
            return shift


    
    def shift_open(self, body):
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
        
    def shift_to_base(self, id):
        ShiftDTO.model_validate(id)
        self.shift_rep.add()
        
    def shifts_body(self, fiscal_code=None, fiscal_date=None):
        return {
            "id": str(uuid.uuid4()),
            "fiscal_code": fiscal_code,
            "fiscal_date": fiscal_date
            }
        
    def load_offline_codes(self, online_mode):
        fiscal_code = self.get_offline_codes()
        if online_mode and fiscal_code < 500:
            self.ask_offline_codes() 
            fiscal_code = self.get_offline_codes()
            # может записать в базу
        return fiscal_code
    
    def cash_status(self):
        cash_id = None
        status = self.cash_online(cash_id)
        if status["offline_mode"]:
            return False
        return True
    
    def receipts_sell(self):
        receipt = ReceiptDTO(
            id=uuid.uuid4(),
            goods=[]
        )

    def shift_status(self, id):
        status = self.universal_api_call(self.api.shift_status(id))
        return status.get("status") == "OPENED"
    
    def shifts(self, body):
        return self.universal_api_call(self.api.shifts(body))

    def go_online(self):
        return self.universal_api_call(self.api.go_online)
    
    def go_offline(self):
        return self.universal_api_call(self.api.go_offline)

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