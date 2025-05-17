
from dataclasses import dataclass
from utils import WorkTimeCntrl, OC_logger
from repository import OrderRep

class Handler:
    def __init__(self, 
                 w_time: WorkTimeCntrl, 
                 ord_rep: OrderRep
                 ):
        self.w_time = w_time
        self.ord_rep = ord_rep
        self.logger = OC_logger.oc_log('analitic_handler')




@dataclass
class Context:
    balance: str = ''