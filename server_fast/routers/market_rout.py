
from fastapi import APIRouter, Depends, \
    HTTPException, Query

from a_service.order_service import OrderServ
from api import EvoClient, RozetMain
from server_flask.flask_app import flask_app, jsonify

from utils import OC_logger

from ..dependencies import get_token_header 
from exceptions.order_exception import AllOrderPayException



router = APIRouter(
    tags=["order"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

# @router.get("/16")
# async def close_day():
#     with flask_app.app_context():
#         ord_cntrl = OrderCntrl()
#         load_order = ord_cntrl.load_confirmed_order()
#         print(load_order, "Test fast api")
#         return jsonify({"message": "Admin getting schwifty"})
    
@router.get("/get_orders")
async def get_orders(api_name: str,
                     store_token: str | None = Query(None)):
    logger = OC_logger.oc_log('get_orders')
    with flask_app.app_context():
        try:
            order_cntrl = OrderServ()
            result = order_cntrl.load_orders_store(api_name, store_token, EvoClient, RozetMain) 
            print("Get orders: ", result)
            if result:
                logger.info(f'Загружено ордер')
                return {"message": "Order get successfuly"}
            return {"message": "All the orders have alredy been download"}
        except Exception as e:
            logger.error(f'Error get orders: {e}')
            return {"message": "Get orders Error"}
    
@router.get("/get_status_unpay")
async def get_status_unpay(api_name: str,
                     store_token: str | None = Query(None)
                     ):
    logger = OC_logger.oc_log('status_unpay')
    with flask_app.app_context():
        try:
            order_cntrl = OrderServ()
            result = order_cntrl.get_status_unpay(api_name, store_token, EvoClient, RozetMain) 
            if result:
                return {"message": "Order get successfuly"}
            return {"message": "All the orders have alredy been download"}
        except AllOrderPayException as e:
            logger.info(f'{e}')
            return {"message": "all order paid"}
        except Exception as e:
            logger.error(f'Error get status pay: {e}')
            return {"error": f"Error get status unpaid {e}"}
    



# @router.get("/")
# async def read_orders():
#     if item_id not in fake_items_db:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"name": fake_items_db[item_id]["name"], "item_id": item_id}

# @router.put(
#     "/{item_id}",
#     tags=["custom"], 
#     responses={403: {"description": "Operation forbidden"}},
# )

# async def update_item(item_id: str):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"
#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}