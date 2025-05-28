


from utils import wrapper
from repository.store_sqlalchemy import StoreRepositorySQLAlchemy

from utils import OC_logger

logger = OC_logger.oc_log('order_serv.store_load_order')

@wrapper()
def load_orders_store(
        market,
        OrderApi,
        add_order3
        ):
    resp = {}
    store = OrderApi(market)
    list_order = store.get_orders()
    print("load_orders_store:", list_order)
    if list_order:
        for order in list_order:
            resp.update(add_order3(order))
            resp.update(store.change_status(order.order_code, 1))
        return resp 
    return False


