from typing import Annotated
from server_flask.flask_app import flask_app
from fastapi.middleware.wsgi import WSGIMiddleware


from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from utils import util_asx
from .dependencies import get_token_header
import uvicorn, multiprocessing, logging

from .routers import order_opers
from .routers import admin

 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Для виведення на консоль
        logging.FileHandler("../common_asx/log/all_app.log"),  # Для запису у файл
    ]
)

OC_log = util_asx.oc_log("fast_api")
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(
    order_opers,
    prefix="/v2/orders",
    tags=["orders"], 
        )
app.include_router(
    admin,
    prefix="/v2/admin",
    tags=["admin"],
)

@app.get("/v2")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    logging.info("Обробка backend server")
    return {"token": token}


def main():
    try:
        uvicorn.run(
            "server_fast.app:app",
            log_level="debug",
            reload=True
        )
    except Exception as e:
        # Запис повідомлення про помилку у журнал
        OC_log.exception("Помилка при створенні екземпляра фаст додатку: %s", e)


try:
    app.mount("/", WSGIMiddleware(flask_app))
except Exception as e:
    # Запис повідомлення про помилку у журнал
    OC_log.exception("Помилка при монтуванні flask_app: %s", e)