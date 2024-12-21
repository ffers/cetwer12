from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from black import CheckCntrl, MarketplaceCntrl


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()
 
@router.get("/check_sign")
async def check_sign():
        check = CheckCntrl()
        check.signinPinCode()
        # print(load_order, "Test fast api")
        return {"message": "Admin getting schwifty"}

@router.get("/market_get_orders")
async def market_sign():
        check = MarketplaceCntrl("Rozet")
        resp = check.get_orders()
        print("відповідь сервера {}".format(resp))
        if resp:
            return 200, {"message": "SUCCESS"}
        # print(load_order, "Test fast api")
        return 200, {"message": "FALSE"}





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