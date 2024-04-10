import os, requests, json, sys
from dotenv import load_dotenv
from intarfaces.send_message_int import MessagingInterface
env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)

class TgClient():
    def __init__(self):
        self.text1 = "Прийнято"
        self.text2 = "Питання"

    def send_message_f(self, chat_id, text, keyboard_json=None):
        method = "sendMessage"
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        url = f"https://api.telegram.org/bot{token}/{method}"
        if keyboard_json:
            data = {"chat_id": chat_id, "text": text, 'parse_mode': 'Markdown', "reply_markup":keyboard_json}
        else:
            data = {"chat_id": chat_id, "text": text}
        resp_json = requests.post(url, data=data).content
        return json.loads(resp_json)


    def answerCallbackQuery(self, callback_query_id, text):
        print(callback_query_id)
        # cache_time = 3
        method = "answerCallbackQuery"
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        url = f"https://api.telegram.org/bot{token}/{method}"
        data = {"callback_query_id": callback_query_id, "text": text} #, "cache_time": cache_time}
        print(data)
        resp = requests.post(url, data=data)
        return resp

    def ForceReply(self, chat_id, callback_query_id=None, text=None):
        print(callback_query_id)
        # cache_time = 3
        method = "sendMessage"
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        url = f"https://api.telegram.org/bot{token}/{method}"
        data = {"chat_id": chat_id, "text": "text", "force_reply": True} #, "cache_time": cache_time}
        print(data)
        resp = requests.post(url, data=data)
        print(resp)
        return resp

    def editMessageText(self, chat_id, message_id, text):
        method = "editMessageText"
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        url = f"https://api.telegram.org/bot{token}/{method}"
        data = {"chat_id": chat_id, "message_id": message_id, "text": text}  # , "cache_time": cache_time}
        print(data)
        resp = requests.post(url, data=data)
        print(resp)
        return resp


    def keyboard_func(self, order_id, delivery_option):
        received = 1
        size_j = sys.getsizeof(received)
        # received_json = json.dumps(received)
        # size_jj = sys.getsizeof(received_json)
        print(size_j)
        # print(size_jj)
        question = 2
        # question_json = json.dumps(question)
        keyboard_json = self.keyboard_generate(self.text1, received, self.text2, question)
        print(keyboard_json)
        size_keyboard = sys.getsizeof(keyboard_json)
        print(size_keyboard)

        return keyboard_json

    def keyboard_generate(self, text1, callback_data1, text2=None, callback_data2=None):
        if text2:
            keyboard = {"inline_keyboard":[[
                {"text": text1, "callback_data": callback_data1},
                {"text": text2, "callback_data": callback_data2}
                ]]}
        else:
            keyboard = {"inline_keyboard":
                [[{"text": text1, "callback_data": callback_data1}]]}
        keyboard_json = json.dumps(keyboard)
        print(keyboard_json)
        return keyboard_json

    def sendPhoto(self, chat_id, photo):
        method = "sendPhoto"
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        url = f"https://api.telegram.org/bot{token}/{method}"
        data = {"chat_id": chat_id, "photo": photo}
        resp_json = requests.post(url, data=data).content
        return json.loads(resp_json)