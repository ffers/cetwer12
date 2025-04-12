from ..parsers.parse_worker import Parse



class Command:
    def __init__(self, **deps):
        self.order_cntrl = deps["OrderCntrl"]()
        self.SourAnCntrl = deps["SourAnCntrl"]()
        self.order_serv = deps["OrderServ"]()
        self.parse = Parse()     

    def execute(self, content):     
        pass      
     