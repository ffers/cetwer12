from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from black import SourAnCntrl, SourDiffAnCntrl
from pydantic import BaseModel
from server_flask.flask_app import flask_app, jsonify


from ..dependencies import get_token_header 

router = APIRouter(
    tags=["analitic"],
    dependencies=[Depends(get_token_header)],
    responses={403: {"description": "Not Authificated"}},
)
  

@router.get("/count_sold")
async def market_sign():   
    api = SourAnCntrl()
    with flask_app.app_context():
        resp = api.sour_diff_all_source_sold("two_days")
        print("відповідь сервера {}".format(resp))
        if resp:
            return 200, {"message": "SUCCESS"}
        # print(load_order, "Test fast api")
        return 200, {"message": "FALSE"}


