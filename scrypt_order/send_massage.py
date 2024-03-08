import os, requests
from dotenv import load_dotenv

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)
class SendMessage():
    def __init__(self):
        pass

    def send_message_f(self, chat_id, text, keyboard_json=None):
        method = "sendMessage"
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        url = f"https://api.telegram.org/bot{token}/{method}"
        if keyboard_json:
            data = {"chat_id": chat_id, "text": text, 'parse_mode': 'Markdown', "reply_markup":keyboard_json}
        else:
            data = {"chat_id": chat_id, "text": text}
        requests.post(url, data=data)

    def answerCallbackQuery(self, callback_query_id, text):
        cache_time = 3
        method = "answerCallbackQuery"
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        url = f"https://api.telegram.org/bot{token}/{method}"
        data = {"callback_query_id": callback_query_id, "text": text, "cache_time": cache_time}
        resp = requests.post(url, data=data)
        return resp