from ..parsers.parse_worker import Parse
from utils import OC_logger
from a_service.analitic.balance_serv.balance_service import BalanceService



class Command:
    def __init__(self, **deps):
        self.order_cntrl = deps["OrderCntrl"]
        self.SourAnCntrl = deps["SourAnCntrl"]()
        self.order_serv = deps["OrderServ"]()
        self.parse = Parse()     
        self.logger = OC_logger.oc_log('source')
        self.analitic = deps["AnaliticServ"]
        self.balance_serv: BalanceService = deps["BalanceService"]

    def execute(self, content):     
        pass      
     