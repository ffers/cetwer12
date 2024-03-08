import os, json, time, logging, pytz
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from api.prom import EvoClient

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
logging.basicConfig(filename='../common_asx/download_orders.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
georgia_timezone = pytz.timezone('Asia/Tbilisi')
value_200_order = f"?limit=100"
file_name = "../common_asx/data.json"


def display_current_time():
    while True:
        current_datetime = datetime.now(timezone.utc) + timedelta(hours=4)
        time.sleep(1)  # Обновлять время каждую секунду
        yield current_datetime


def write_json_func():
    time_now = next(display_current_time())
    time_now_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
    AUTH_TOKEN = os.getenv("PROM_TOKEN")
    # Initialize Client
    if not AUTH_TOKEN:
        raise Exception('Sorry, there\'s no any AUTH_TOKEN!')
    api_example = EvoClient(AUTH_TOKEN)
    order_list = api_example.get_order_list(value_200_order)
    if order_list is None:
        return print(time_now_str, "Сталася помилка під час виконання запиту.")
    if not order_list['orders']:
        raise Exception('Sorry, there\'s no any order!')
    else:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(order_list, file, indent=4, ensure_ascii=False)

        print(time_now_str, "Ордери загружено")
        logging.info("Ордери загружено!")



