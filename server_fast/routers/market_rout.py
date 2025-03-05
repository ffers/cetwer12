from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException

from black.order_controller.get_order import GetOrder
from server_flask.flask_app import flask_app, jsonify


from ..dependencies import get_token_header 


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
async def close_day():
    with flask_app.app_context():
        api = GetOrder("rozetka")
        result = api.get_orders()
        print("Get orders: ", result)
        if result:
            return {"message": "Order get successfuly"}
        return {"message": "All the orders have alredy been download"}


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