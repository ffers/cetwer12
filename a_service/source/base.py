


from a_service import SourDiffAnServ
from repository import SourDiffAnRep
from a_service import CacheService
from utils import WorkTimeCntrl, OC_logger, DEBUG
from repository import OrderRep
from repository import ProductRep



class ContextDepend:
    def __init__(self,
                w_time: WorkTimeCntrl,
                diff_process: SourDiffAnServ,
                diff_rep: SourDiffAnRep,
                cach_serv_dont_need: CacheService,
                order_rep: OrderRep,
                prod_rep: ProductRep,
                log: OC_logger,
                 ):
        self.w_time = w_time
        self.diff_rep = diff_rep
        self.prod_rep = prod_rep
        self.diff_process = diff_process
        self.cach_serv_dont_need = cach_serv_dont_need
        self.log = log
        self.DEBUG = DEBUG


class Source:
    def __init__(self, ctx: ContextDepend):
        self.ctx = ctx