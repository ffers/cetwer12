import os
from typing import Union
from fastapi import FastAPI, Request, Header
from pydantic import BaseModel
from dotenv import load_dotenv
from black import TelegramController

tg_cntrl = TelegramController()

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)

app_fast = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app_fast.get("/")
def read_root():
    return {"Hello": "World"}


@app_fast.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}", include_in_schema=False)
# def bot():
#     if request.method == 'POST':
#         data = request.json
#         print(request.json)
#         try:
#             button_hand(data)
#             # aw_cl.await_tg_button(data)
#         except:
#             print("не вдалося отримати відповідь")
#         return {'ok': True}
#     return render_template('index.html', user=current_user)

@app_fast.post("/bot")
def bot_request(data: dict, x_telegram_bot_api_secret_token: str = Header(None)):
    print(data, x_telegram_bot_api_secret_token)
    token = os.getenv("X_TELEGRAM_API_BOT_TOKEN")
    if x_telegram_bot_api_secret_token == token:
        print(data, x_telegram_bot_api_secret_token)
        resp = tg_cntrl.await_telegram(data)
        return {"success": True}
    else:
        return {"success": False}


