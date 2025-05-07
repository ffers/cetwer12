

import os

from fastapi import APIRouter, Depends, \
    HTTPException, Query
from server_flask.flask_app import flask_app, jsonify
from server_flask.db import db

from a_service.order_service import OrderServ, OrderApi
from a_service import EvoService, RozetkaServ, TgServNew
from a_service.order_service.handlers.base import UnpayContext



from api import EvoClient, RozetMain, TgClient
from repository.store_sqlalchemy import StoreRepositorySQLAlchemy
from repository import OrderRep

from utils import OC_logger

from ..dependencies import get_token_header 
from exceptions.order_exception import *



logger = OC_logger.oc_log('market_rout')

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
    with flask_app.app_context():
        try:
            order_cntrl = OrderServ(store_repo=StoreRepositorySQLAlchemy(db.session))
            result = order_cntrl.load_orders_store_v2(
                api_name, 
                store_token, 
                EvoClient, 
                RozetMain,
                ) 
            print("Get orders: ", result)
            if result:
                logger.info(f'Загружено ордер')
                return {"message": "Order get successfuly"}
            return {"message": "All the orders have alredy been download"}
        except Exception as e:
            logger.error(f'Error get orders: {e}')
            return {"message": "Get orders Error"}
    
@router.get("/get_status_unpay")
async def get_status_unpay(source_token: str,
                     store_token: str | None = Query(None)
                     ):
    with flask_app.app_context():
        try:
            tg_token = os.getenv('TELEGRAM_BOT_TOKEN')
            evo_serv = EvoService(EvoClient(store_token))
            roz_serv = RozetkaServ(RozetMain(store_token))
            tg_serv = TgServNew(TgClient(tg_token))
            order_repo = OrderRep(db.session)
            store_repo = StoreRepositorySQLAlchemy(db.session)
            store_proc = OrderApi
            order_serv = OrderServ(
                evo_serv=evo_serv, 
                roz_serv=roz_serv,
                tg_serv=tg_serv,
                order_repo=order_repo,
                store_repo=store_repo, 
                )
            ctx = UnpayContext(
                            evo_serv,
                            roz_serv,
                            tg_serv,
                            order_repo,
                            store_repo,
                            OC_logger.oc_log('unpay_test'),
                            store_proc,

                )
            ctx.state.token = source_token
            result = order_serv.get_status_unpay_v3(ctx) 
            if result:
                return {"message": "Order get successfuly"}
            return {"message": "All the orders have alredy been download"}
        except AllOrderPayException as e:
            return {"message": "all order paid"}
        except OrderNotPaidException as e:
            return {"info": f"Error get status unpaid"}
        except Exception as e:
            logger.error(f'Unhandled error: {e}')
            return {"error": f"Error unhandled for get status unpaid"}
    



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