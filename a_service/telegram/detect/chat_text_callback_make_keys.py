# якщо це чат менеджер або курьер або склад або каштан
# то опрацьовується текст та колбек квері
# 
# 
# виведення ключів text.get(something, None)
# набор ключів FlagStrategy

# потім перевірка на чати
# можливо ще допущені користувачи на майбутне 
# потім на команди команди вже будуть різними
# в ідеалі булоб привести все до однакових дій менше роботи

from settings import Settings


class Way:
    def __init__(self, message, callback):
        self.message = message
        self.callback = callback

# check for message or call_back
class CheckAvaliable(Way):
    def execute(self, data):
        if "callback_query" in data:
            return self.callback(data)
        if "message" in data: #працює з усіма відповдями
            text = data.get("message", None)
            return FactoryCommand.get_command(text)
            # button_hand(data)
        return '', 200
    
class FactoryCommand:
    @staticmethod
    def get_command(text):
        commands = {
            "#взял": "take",
            "#склад": "stock",
            "#редактируєм": "edit",
            "#прихід": "arrival",
            "#коментар":"comment"
        }
        for command, action in commands.items():
            if command in text.lower():
                return action
            else:
                None

class ButtonCommandFactory:
    @staticmethod
    def create_command(data_keyb):
        commands = {
            "1": ConfirmOrderCommand,
            "2": QuestionOrderCommand
        }
        if data_keyb in commands:
            return commands[data_keyb]()
        return None