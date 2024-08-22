import json, sys

# status підтвердження: 137639; питання: 142216

class TgKeyboard():
    def __init__(self):
        self.text1 = "Прийнято"
        self.text2 = "Питання"

    def keyboard_func(self, order_id, delivery_option):
        received = {"status": "received"}
        size_j = sys.getsizeof(received)
        received_json = json.dumps(received)
        size_jj = sys.getsizeof(received_json)
        print(size_j)
        print(size_jj)
        question = {"custom_status_id": 142216}
        question_json = json.dumps(question)
        keyboard_json = self.keyboard_generate(self.text1, received_json, self.text2, question_json)
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


