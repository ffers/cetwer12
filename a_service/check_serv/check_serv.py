import uuid, time
from datetime import datetime, timezone
from repository import UserTokenRep

from DTO import UserTokenDTO, ReceiptDTO, ShiftDTO
from repository import ReceiptRep, ShiftRep
from api import CheckboxClient
from .authorization import Authorization
from .api_call import ApiCall

'''
Управление смени нужно ручное
также по расписанию

Перевірити касса онлайн чи офлайн Раз в 2 хвилини (Планировщик)
'''
 
class CheckServ(object):
    def __init__(self, user_id):
        from black import TelegramController 
        self.tg = TelegramController()
        self.user_id = user_id
        self.auth = Authorization(user_id, CheckboxClient, TelegramController)
        self.token = self.auth.check_token()
        self.token_rep = UserTokenRep(None)
        self.receipt_rep = ReceiptRep()
        self.shift_rep = ShiftRep()
        self.api_call = ApiCall(CheckboxClient, self.token)


    def cash_register_operating(self):
        resp = self.api_call.cash_registers()
        print("cash_register_operating:", self.token)
        print("cash_register_operating:", resp)
        cash_online = self.cash_online_check()
    #    if cash_online:
    #         online = self.online_mode()
    #         if online:
    #             pass
    #     if not cash_online:
    #         ping = self.try_online()
    #         if ping:
    #             cash_online = self.cash_online_check()
    #             if cash_online:
    #                 self.online_mode()
    #         else:
    #             self.offline_mode() 

    def cash_online_check(self):
        self.cash_online = None

    
    def validate_error(self, resp):
        if "error" in resp: # додати обробку різних помилок
                msg = ">>> {}".format(resp["error"])
                send = self.tg.sendMessage(self.tg.chat_id_info, msg)
                return True
        return False
    

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
        load_shift = self.shift_rep.load_shift_open()
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
                    return self.add_shifts_base(status)
                time.sleep(2)
                times += 1
            else:
                raise Exception(f"Змінна не відкрилася {body}")     
        except Exception as e:
            self.tg.sendMessage(self.tg.chat_id_info, str(e))
            return False   
    
    def add_shifts_base(self, data):
        ShiftDTO(
            shifd_id=data["id"],
            open=data["opened_at"],
            closed=data["closed_at"]
        )
        return self.shift_rep.add()

    def update_shifts_base(self, data):
        d = ShiftDTO(
            shifd_id=data["id"],
            open=data["opened_at"],
            closed=data["closed_at"]
        )
        return self.shift_rep.update(d)

    
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

    def shift_status_tax(self, id):
        status = self.universal_api_call(self.api.shift_status(id))
        return status.get("status") == "OPENED"
    
    def shift_status_crm(self) -> bool:
        shifts_list = self.shift_rep.load_shift_open()
        if shifts_list:
            return True
        

    

        



