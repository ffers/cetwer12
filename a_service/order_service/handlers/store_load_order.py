


from utils import wrapper
from repository.store_sqlalchemy import StoreRepositorySQLAlchemy

from utils import OC_logger

logger = OC_logger.oc_log('order_serv.store_load_order')

@wrapper()
def load_orders_store(
        item_token, 
        token, 
        EvoClient, 
        RozetMain,
        OrderApi,
        map_ord,
        add_order3,
        store_repo: StoreRepositorySQLAlchemy
        ):
    resp = {}
    store_data = store_repo.get_token(item_token)
    print('store_data', store_data)
    store = OrderApi(store_data.api, token, EvoClient, RozetMain)
    list_order = store.get_orders()
    print("load_orders_store:", list_order)
    if list_order:
        for order in list_order:
            mapper = map_ord(store_data, order)
            dto = mapper.process()
            resp.update(add_order3(dto))
            resp.update(store.change_status(dto.order_code, 1))
        return resp 
    else:
        return {"success": "ok", "order": "Store empty"}