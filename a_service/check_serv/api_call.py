from .parser_api_call import ParserApiCall


class ApiCall:
    def __init__(self, CheckboxClient, token):
        self.api = CheckboxClient(token)
        self.pars = ParserApiCall()

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
    
    def check_cash_online(self, id):
        data = self.universal_api_call(self.api.cash_online(id))
        return self.pars.parse_check_cash_online(data)
    
    def ping_tax_service(self):
        data = self.universal_api_call(self.api.ping_tax_service)
        return self.pars.parse_ping_tax(data)
    
    def universal_api_call(self, func, *args, **kwargs):
        # try:
            resp = func(*args, **kwargs)
            success = self.validate_error(resp)
            # if not success:
        #     raise 
            return resp 
        # except Exception as e:
        #     return False 

    def validate_error(self, resp):
        if "error" in resp: # додати обробку різних помилок
                return ">>> {}".format(resp["error"])
        return False
    

    


