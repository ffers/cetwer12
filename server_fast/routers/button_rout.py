from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from typing import Annotated
from pydantic import BaseModel

from server_flask.flask_app import flask_app, jsonify

from ..dependencies import get_token_header 

router = APIRouter(
    tags=["button"],
    dependencies=[Depends(get_token_header)],
    responses={403: {"description": "Not Authificated"}},
)

async def process_market_sign(method_name: str):
    api = RegSchedulleSrv()
    with flask_app.app_context():
        method = getattr(api, method_name)  # Динамічний виклик методу
        resp = method()
        print(f"Відповідь сервера: {resp}")
    
    return JSONResponse(status_code=200, content={"message": "SUCCESS" if resp else "FALSE"})


@router.get("/start_16_58")
async def market_sign():   
    return await process_market_sign("reg_16_58")
    

    




