from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from utils import util_asx

import uvicorn, multiprocessing, logging
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

@app.get("/v2")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):

    logging.info("Обробка backend server")

    return {"token": token}

def main():
    try:
        uvicorn.run(
            "server_flask.flask_app:app",
            log_level="debug",
            reload=True
        )
    except Exception as e:
        # Запис повідомлення про помилку у журнал
        OC_log.exception("Помилка при створенні екземпляра фаст додатку: %s", e)