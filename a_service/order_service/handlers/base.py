from domain.models.store_dto import StoreDTO
from ...evo_service.evo_service import EvoService
from ...rozetka_serv import RozetkaServ
from ...telegram_service import TgServNew
from ..order_api_process import OrderApi
from repository import OrderRep
from repository import StoreRepositorySQLAlchemy
from utils import OC_logger

class UnpayState:
    store = None
    token = None
    store_api = None
    orders = []

class UnpayContext:
    def __init__(
            self,
            evo_serv: EvoService,
            roz_serv: RozetkaServ,
            tg_serv: TgServNew,
            order_repo: OrderRep,
            store_repo: StoreRepositorySQLAlchemy,
            logger: OC_logger.oc_log,
            store_proc: OrderApi
        ):
        self.evo_serv = evo_serv
        self.roz_serv = roz_serv
        self.tg_serv = tg_serv
        self.order_repo = order_repo
        self.store_repo = store_repo
        self.logger = logger
        self.store_proc = store_proc
        self.state = UnpayState()
        self.vldt_order = None
        self.store_id = None


class Handler:
    def __init__(self, context: UnpayContext):
        self.ctx = context
        self.logger = context.logger
        

    def execute(self, data):
        raise NotImplementedError("Handler must implement `execute()`")


