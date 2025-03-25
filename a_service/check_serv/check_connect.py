
from .api_call import ApiCall
from .authorization import Authorization

from dataclasses import dataclass

@dataclass
class ConnectData:
    auth: bool
    ping_tax: bool
    cash_online: bool
    offline_codes: bool
    shifts: bool

class Connect:
    def __init__(self):
        self.con = ConnectData()
        self.auth = Authorization()
        self.call = ApiCall()

    def process(self):
        pass

class CheckAuth(Connect):
    def process(self):
        self.con.auth = self.auth.connect
        return True

class CheckPingTaxService(Connect):
    def process(self):
        self.con.ping_tax = self.call.ping_tax_service()
        return True

class CheckCashOnline(Connect):
    def process(self):
        self.con.cash_online = self.call.check_cash_online(1) # you must change id
        return True
    
class CheckOfflineCodes(Connect):
    def process(self):
        self.con.offline_codes = self.call.get_offline_codes()
        return True

class CheckShifts(Connect): # ????
    def process(self):
        self.con.shifts = self.call.shifts()
        return True

class Builder:
    def __init__(self):
        self.commands = [
            CheckAuth,
            CheckPingTaxService,
            CheckCashOnline,
            CheckOfflineCodes,
            CheckShifts
        ]

    def add_command(self, command_class):
        self.commands.append(command_class)
        return self

    def build(self, data):
        pointer = None
        for cmd_class in self.commands:
            pointer = cmd_class(data).execute()
            print(pointer, "builder")
        return pointer
