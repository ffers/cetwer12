
from dataclasses import dataclass
from utils import WorkTimeCntrl, OC_logger
from repository import OrderRep, AnaliticRep, ProductRep, SourceRep, \
    BalanceRepositorySQLAlchemy
from black import AnCntrl
from decimal import Decimal
from domain.models.analitic_dto import AnaliticDto


class ContextDepend:
    def __init__(self, 
                 w_time: WorkTimeCntrl, 
                 ord_rep: OrderRep,
                 an_cntrl: AnCntrl,
                 an_rep: AnaliticRep,
                 logger: OC_logger.oc_log,
                 prod_rep: ProductRep,
                 source_rep: SourceRep,
                 state: AnaliticDto,
                 balance_rep: BalanceRepositorySQLAlchemy,
                 source_an_cntrl # нужен для обработки склада пока нет собственой функции
                 ):
        self.w_time = w_time
        self.ord_rep = ord_rep
        self.an_cntrl = an_cntrl
        self.an_rep = an_rep
        self.logger = logger
        self.prod_rep = prod_rep
        self.source_rep = source_rep
        self.state = state
        self.balance_rep = balance_rep
        self.source_an_cntrl = source_an_cntrl

class Handler:
    def __init__(self, ctx: ContextDepend):
        self.ctx = ctx

    def format_float(self, num):
        try:
            if isinstance(num, int):
                num_format = str(f"{int(num)}.00")
                # Конвертуємо int у Decimal
                return Decimal(num_format)
            else:
                num_format = float(num)
                # Конвертуємо float у Decimal
                return Decimal(str(f"{num_format: .2f}"))
        except Exception as e:
            self.ctx.logger.error(f'Проблема format_float: {e}')




