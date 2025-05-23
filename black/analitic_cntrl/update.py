


from server_flask.db import db
from black import ProductAnaliticControl
from black import AnCntrl
from black import SourAnCntrl
from black import SourDiffAnCntrl
from utils import OC_logger, WorkTimeCntrl
from asx.a_service.analitic.analitic_day.analitic_day import CountAnaliticV2 
from a_service.analitic.base import ContextDepend

from domain.models.analitic_dto import AnaliticDto

from repository import OrderRep, AnaliticRep, ProductRep, \
    SourceRep, BalanceRepositorySQLAlchemy




class Update:
    def cntrl(self):
        ctx = ContextDepend(
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
        resp = CountAnaliticV2(
                ctx
            ).day()
        print(f'{resp =}')
        return resp