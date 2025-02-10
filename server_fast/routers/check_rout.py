from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from black import CheckCntrl
from pydantic import BaseModel
from server_flask.flask_app import flask_app, jsonify


from ..dependencies import get_token_header 

router = APIRouter(
    tags=["check"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/check_sign")
async def check_sign():
    with flask_app.app_context():
        check = CheckCntrl(1)
        bool = check.start()
        if bool:
            return {"message": "Admin getting successful"}
        return {"message": "Unsuccessful"}