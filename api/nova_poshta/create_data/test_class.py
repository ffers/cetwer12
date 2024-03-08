import os, json, requests, time
from os.path import join, dirname
from requests.exceptions import ReadTimeout
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

current_datetime = datetime.now(timezone.utc) + timedelta(hours=4)
date_today = current_datetime.strftime("%d.%m.%Y")
date_yesterday_nf = current_datetime - timedelta(days=7)
date_yesterday = date_yesterday_nf.strftime("%d.%m.%Y")
date_7day_nf = current_datetime - timedelta(days=1)
date_7day = date_7day_nf.strftime("%d.%m.%Y")
api_url = "https://api.novaposhta.ua/v2.0/json/"
filename = current_datetime.strftime("%Y-%m-%d_%H%M%S")
ttn_json_f_n = "dovidka/dov_" + filename + ".json"
stat_json_f_n = filename + "st.json"
folder_path = "dovidka"
files = os.listdir(folder_path)

class NpClient(object):

    def __init__(self):
        pass

    def date_today_np(self):
        while True:
            current_datetime = datetime.now(timezone.utc) + timedelta(hours=4)
            date_today = current_datetime.strftime("%d.%m.%Y")
            yield date_today
            print(f"Текущее время: {date_today}")
            time.sleep(1)  # Обновлять время каждую секунду

    def get_from_env(self, key):
        dotenv_path = join(dirname(__file__), '../.env')
        load_dotenv(dotenv_path)
        print()
        return os.environ.get(key)

    def json_read_dict(self, file):
        with open(file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    def prenit_test(self):
        np_date_gen = self.date_today_np()
        for _ in range(1):
            print(next(np_date_gen))
        print(self.get_from_env("NP_TOKEN"))

np_client = NpClient()
np_client.prenit_test()
