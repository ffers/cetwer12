from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from black import CheckCntrl, MarketplaceCntrl
from pydantic import BaseModel

from ..dependencies import get_token_header 

router = APIRouter(
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
  
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

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None



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