from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

import uvicorn, multiprocessing, logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Для виведення на консоль
        logging.FileHandler("../common_asx/log/all_app.log"),  # Для запису у файл
    ]
)


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/v2")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):

    logging.info("Обробка backend server")

    return {"token": token}

def main():
    uvicorn.run(
        "server_flask.flask_app:app",
        log_level="debug",
        reload=True
    )