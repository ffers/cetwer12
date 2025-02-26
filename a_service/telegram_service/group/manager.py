from ..parsers.parse_text import ParseText
from ..parsers.parse_message import ParseMsgFactory
from a_service.telegram_service.parsers.color_bot_rep import ProductCounBot
from ..parsers.parse_color import TextColorParser

class Command:
    def __init__(self, PT: ParseText, PM: ParseMsgFactory):
        self.text_p = PT()
        self.msg_p = PM()


    def execute(self, chat_data):
        pass
          
class NewOrders(Command):
    def execute(self, chat_data):
        return chat_data
    
# 🔹 Клас, що виконує команду
class CommandHandler:
    @staticmethod
    def factory(chat_data):
        commands = {
            "new_orders": NewOrders,
        } 
        if chat_data.cmd in commands:
            return commands[chat_data.cmd](
                ParseText, ParseMsgFactory
                ).execute(chat_data)
        return f"Немає команди {chat_data.cmd}"
            



