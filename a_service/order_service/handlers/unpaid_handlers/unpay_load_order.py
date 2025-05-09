
from DTO import OrderDTO
from domain.models.store_dto import StoreDTO
from ..base import Handler, UnpayContext
from exceptions.order_exception import *
from .unpay_work import ValidateUnpayOrderHandler, OrderProcessor
from utils import OC_logger

class StoreUnvaliableException(Exception):
    pass

class LoadStore(Handler):
    def execute(self):
        print('LoadStore:', self.ctx)
        token = self.ctx.state.token
        print(token)
        store = self.ctx.store_repo.get_token(token)
        if not store:
            raise StoreUnvaliableException('Джерело не знайдено')
        self.ctx.state.store = store
        return store.id
    
class LoadUnpaid(Handler):
    def execute(self):
        store_id = self.ctx.state.store.id
        self.logger.debug(f'store_id: {store_id}')
        orders = self.ctx.order_repo.load_unpaid_prom_orders(store_id)
        if not orders:
            raise AllOrderPayException('Несплачені замовлення не знайдено')
        self.ctx.state.orders = orders
    


class UnpayLoad:
    def __init__(self):
        self.commands = []
        self.logger = OC_logger.oc_log('order_serv.unpay_load_order')

    def add_command(self, command_class):
        self.commands.append(command_class)
        return self

    def build(self, context):  
            for cmd_class in self.commands:
                self.logger.debug(f"Працює: {cmd_class.__name__}")
                cmd_class(context).execute()
            return context
    

class UnpayLoadOrderHandler:
    def __init__(self, ctx):
        self.ctx = ctx
        self.pipeline = (
            UnpayLoad()
            .add_command(LoadStore)
            .add_command(LoadUnpaid)
        )

    def handle(self):
        return self.pipeline.build(self.ctx)
    
class UnpayLoadOrderProcessor:
    def __init__(
            self, ctx: UnpayContext
    ):
        self.ctx = ctx
        self.oloh = UnpayLoadOrderHandler(ctx)
        self.op = OrderProcessor(ValidateUnpayOrderHandler(ctx))

    def process(self):
        self.oloh.handle()
        resp = self.op.handle_all(self.ctx.state.orders)
        return resp


