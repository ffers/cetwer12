
from ...base import Handler



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
    
    def execute2(self):
        store_id = self.ctx.state.store.id
        orders = self.ctx.order_repo.load_unpaid_prom_orders(store_id)
        if not orders:
            raise AllOrderPayException('Замовлення не знайдено')
        self.ctx.state.orders = orders


    def handle_all(self, orders):
        results = []
        for order in orders:
            try:
                result = GetApi(self.ctx).execute(order)
                results.append(result)
            except Exception as e:
                self.logger.error(f'❌ Order {order.order_code}: {e}')
                raise
        return results
    

class GetApi(Handler):
    def execute(self, order):
        api = self.ctx.state.store.api
        apis = {
                "rozetka": self.ctx.roz_serv,
                "prom": self.ctx.evo_serv
        }
        if api in apis:
            self.ctx.state.store_api = apis[api]
        else:
            raise ValueError(f"We dont have api: {api}")  
        
class GetOrderStore(Handler):
    def execute(self, order):
        self.logger.info(f'Перевіряємо замовлення: {order.order_code}')
        order_store = self.ctx.state.store_api.get_order(order.order_code)
        return self.order_mapper(order_store, order)
    
class ChangeOrder(Handler):
    def execute(self, order):
        resp = self.ctx.order_repo.update_payment_status(order.id, 1)
        if not resp:
            self.logger.error(f'Помилка зміни статусу: {order.order_code}')
            raise OrderNotUpdateStatusException(f'Помилка зміни статусу {order.order_code}') # щось інше треба відповісти
        return resp
    

class SendManager(Handler):
    def execute(self, order):
        resp = self.ctx.tg_serv.sendMessage(self.ctx.tg_serv.chat_id_confirm, f'Оплачeно замовлення {order.order_code}')
        if not resp:
            self.logger.error(f'Помилка відправкі менеджеру: {order.order_code}')
            raise TGsendMessageException(f'Помилка відправкі менеджеру {order.order_code}')
        return True



def register():
    def decorator(cls):
        print(cls)
        return cls
    return decorator