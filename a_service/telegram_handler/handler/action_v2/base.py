from ..parsers.parse_worker import Parse
from utils import OC_logger



class Command:
    def __init__(self, **deps):
        self.order_cntrl = deps["OrderCntrl"]
        self.SourAnCntrl = deps["SourAnCntrl"]()
        self.order_serv = deps["OrderServ"]()
        self.parse = Parse()     
        self.logger = OC_logger.oc_log('source')

    def execute(self, content):     
        pass      
     