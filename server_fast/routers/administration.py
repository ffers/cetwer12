from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from black import CheckCntrl, MarketplaceCntrl

from black import OrderCntrl
from server_flask.flask_app import flask_app
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()
 
@router.get("/check_sign")
async def check_sign():
        check = CheckCntrl()
        check.signinPinCode()
        # print(load_order, "Test fast api")
        return {"message": "Admin getting schwifty"}

@router.get("/rozetka_sign")
async def market_sign():
        check = MarketplaceCntrl("Rozet")
        check.get_orders()
        # print(load_order, "Test fast api")
        return {"message": "Admin getting schwifty"}





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