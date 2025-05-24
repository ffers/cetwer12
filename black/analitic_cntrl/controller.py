


from server_flask.db import db
from black import ProductAnaliticControl
from black import AnCntrl
from black import SourAnCntrl
from black import SourDiffAnCntrl
from utils import OC_logger, WorkTimeCntrl
from a_service.analitic.analitic_day.analitic_day import CountAnaliticV2 
from a_service.analitic.analitic_day.period_v2 import PeriodV2

from a_service.analitic.base import ContextDepend

from domain.models.analitic_dto import AnaliticDto

from repository import OrderRep, AnaliticRep, ProductRep, \
    SourceRep, BalanceRepositorySQLAlchemy

class Controller:
    def __init__(self):
        self.ctx = ContextDepend(
            w_time=WorkTimeCntrl(),
            ord_rep=OrderRep(),
            an_cntrl=AnCntrl(),
            an_rep=AnaliticRep(),
            logger=OC_logger.oc_log('analitic_handler'),
            prod_rep=ProductRep(),
            source_rep=SourceRep(),
            state=AnaliticDto,
            balance_rep=BalanceRepositorySQLAlchemy(db.session),
            source_an_cntrl=SourAnCntrl()
        )
        self.log = OC_logger.oc_log('analitic.controller')

    async def day(self):
        try: 
            resp = CountAnaliticV2(
                    self.ctx
                ).day()
            print(f'{resp =}')
            return resp
        except Exception as e:
            self.log.exception(f'day -  {e}')
            return False

    
    async def week(self):
        try: 
            resp = PeriodV2(
                    self.ctx
                ).process('week', 'day')
            print(f'{resp =}')
            return resp
        except Exception as e:
            self.log.exception(f'period -  {e}')
            return False

    async def month(self):
        try: 
            resp = PeriodV2(
                    self.ctx
                ).process('month', 'week')
            print(f'{resp =}')
            return resp
        except Exception as e:
            self.log.exception(f'period -  {e}')
            return False
        
    async def all(self):
        try:
            resp = CountAnaliticV2(
                    self.ctx
                ).day()
            resp = PeriodV2(
                    self.ctx
                ).process('week', 'day')
            resp = PeriodV2(
                    self.ctx
                ).process('month', 'week')
            resp = PeriodV2(
                    self.ctx
                ).process('year', 'month')
            resp = PeriodV2(
                    self.ctx
                ).process('all', 'year')
            return resp
        except Exception as e:
            self.log.exception(f'period -  {e}')
            return False