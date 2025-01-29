import os
from a_service import CheckServ


class CheckCntrl(object):
    def __init__(self, user_id):
        self.user_id = user_id
        
    def start(self):
        check = CheckServ(self.user_id)
        resp = check.cash_registers()
        return resp
    
    
 




