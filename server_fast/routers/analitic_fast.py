from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from asx.black.analitic_cntrl.analitic_cntrl import AnaliticCntrlV2

from typing import Annotated
from pydantic import BaseModel

from server_flask.flask_app import flask_app, jsonify

from black import SourAnCntrl, SourDiffAnCntrl
from scrypt_order import RegSchedulleSrv

from utils import OC_logger

from ..dependencies import get_token_header 

router = APIRouter(
    tags=["analitic"],
    dependencies=[Depends(get_token_header)],
    responses={403: {"description": "Not Authificated"}},
)

logger = OC_logger.oc_log('fast.analitic_rout')

async def process_market_sign(func_name: str):
    with flask_app.app_context():
        reg_serv = RegSchedulleSrv()
        resp = None
        try:
            func = getattr(reg_serv, func_name) 
            resp = func()
            logger.info(f'Відповідь {func_name}: {resp}')
            print(f"Відповідь сервера: {resp}")
            return JSONResponse(status_code=200, content={"message": "SUCCESS" if resp else "FALSE"})
        except Exception as e:
            logger.exception(f'{e}')
            return jsonify({'error':  f'{func_name}: False'})

@router.get("/count_sold")
async def market_sign():   
    api = SourAnCntrl()
    with flask_app.app_context():
        resp = api.sour_diff_all_source_sold("two_days")
        print("відповідь сервера {}".format(resp))
        if resp:
            return 200, {"message": "SUCCESS"}
        return 200, {"message": "FALSE"}
    
@router.get("/start_16_58")
async def market_sign():   
    return await process_market_sign("reg_16_58")

@router.get("/close_group")
async def market_sign():   
    return await process_market_sign("close_group")
    
@router.get("/start_17_00")
async def market_sign():   
    return await process_market_sign("reg_17_00")
    
@router.get("/start_20_00")
async def market_sign():   
    return await process_market_sign("reg_20_00")
    
@router.get("/start_20_01")
async def market_sign(): 
    return await process_market_sign("reg_20_01")

@router.get("/update_analitic")
async def market_sign():
    with flask_app.app_context():
        cntrl = AnaliticCntrlV2()
        return await cntrl.all() 
    
@router.get("/report")
async def market_sign():
    with flask_app.app_context():
        cntrl = AnaliticCntrlV2()
        return await cntrl.report() 
    
@router.get("/diff_count_sold")
async def market_sign():
    with flask_app.app_context():
        cntrl = AnaliticCntrlV2()
        return await cntrl.diff_count_sold() 




