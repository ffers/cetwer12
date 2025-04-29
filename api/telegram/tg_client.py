import os, requests, json, sys, re
from dotenv import load_dotenv
from intarfaces.send_message_int import MessagingInterface

env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)

class TgClient():
    def __init__(self):
        self.text1 = "Прийнято"
        self.text2 = "Скасувати"
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")

    def send_message_f(self, chat_id, text, keyboard_json):
        escape_text = self.escape_text(text)
        method = "sendMessage"
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        url = f"https://api.telegram.org/bot{token}/{method}"
        if keyboard_json:
            data = {"chat_id": chat_id, "text": escape_text, 'parse_mode': 'MarkdownV2', "reply_markup":keyboard_json}
        else:
            data = {"chat_id": chat_id, "text": escape_text, 'parse_mode': 'MarkdownV2'}
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

    def forceReply(self, chat_id, callback_query_id, text):
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

    def deleteMessage(self, chat_id, message_id):
        method = "deleteMessage"
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        url = f"https://api.telegram.org/bot{token}/{method}"
        data = {"chat_id": chat_id, "message_id": message_id}  # , "cache_time": cache_time}
        print(data)
        resp = requests.post(url, data=data)
        print(resp)
        return resp


    def keyboard_func(self):
        size_j = sys.getsizeof(1)
        keyboard_json = self.keyboard_generate(self.text1, 1, self.text2, 2)
        print(keyboard_json)
        return keyboard_json

    def keyboard_generate(self, text1, callback_data1, text2, callback_data2):
        if text2:
            keyboard = {"inline_keyboard":[[
                {"text": text1, "callback_data": callback_data1},
                {"text": text2, "callback_data": callback_data2},
                {"text": "Дубль", "callback_data": 3}
                ]]}
        else:
            keyboard = {"inline_keyboard":
                [[{"text": text1, "callback_data": callback_data1}]]}
        keyboard_json = json.dumps(keyboard)
        print(keyboard_json)
        return keyboard_json

    def sendPhoto(self, chat_id, photo):
        method = "sendPhoto"

        url = f"https://api.telegram.org/bot{self.token}/{method}"
        data = {"chat_id": chat_id, "photo": photo}
        resp_json = requests.post(url, data=data).content
        if json.loads(resp_json)["ok"]:
            return json.loads(resp_json)
        else:
            load = self.loadPhoto(chat_id)
            return load



    def loadPhoto(self, chat_id):
        file = r"/home/ff/python_program/dev_asx/asx/server_flask/static/images/OS.png"

        files = {
            'photo': open(file, 'rb')
        }
        print(files)
        message = ('https://api.telegram.org/bot' + self.token + '/sendPhoto?chat_id='
                   + chat_id)
        send = requests.post(message, files=files).content
        print(send)
        return send

    def escape_text(self, text):
        two_slash = r"_*[]~`>#|{}.!-.()+="
        one_slash = r"-.()+="
        escape_two_slash = re.sub(f"([{re.escape(two_slash)}])", r"\\\1", text)
        escape_one_slash = re.sub(r'(?<!\\)([-.()+=])', r'\\\1', escape_two_slash)
        # return re.sub(r'\\([^\w\s])', r'\1', escape_two_slash)
        return escape_one_slash



tg_api = TgClient()