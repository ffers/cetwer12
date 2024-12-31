
import os

from typing import Annotated

from fastapi import Header, HTTPException


async def get_token_header(authorization: Annotated[str, Header()]):
    if authorization != os.getenv("SEND_TO_CRM_TOKEN"):
        print(authorization)
        print("Disconect")
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    


async def get_query_token(token: str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")