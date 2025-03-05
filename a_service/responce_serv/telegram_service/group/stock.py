from ..parsers.parse_text import ParseText
from ..parsers.parse_message import ParseMsgFactory
from ..parsers.parse_color import TextColorParser

class Command:
    def __init__(self, PT: ParseText, PM: ParseMsgFactory):
        self.text_p = PT()
        self.msg_p = PM()


    def execute(self, chat_data):
        pass
          
class TextParseColor(Command):
    def execute(self, chat_data):
        pointer = TextColorParser().manager_bot(chat_data)
        # result = ProductCounBot().manager_bot(text)
        print(pointer, "ProductCounBot")
        # получить текст и распарсить и посчитать
        return pointer # має повернути команду, чат, готовий дікт, та відповідь можливо
    
# 🔹 Клас, що виконує команду
class CommandHandler:
    @staticmethod
    def factory(chat_data):
        commands = {
            # "take": "take",
            "stock": TextParseColor,
            # "edit": "edit",
            # "arrival": "ArrivalCommand,",
            # "comment":"comment"
        } 
        if chat_data.cmd in commands:
            return commands[chat_data.cmd](
                ParseText, ParseMsgFactory
                ).execute(chat_data)
        return f"Немає команди {chat_data.cmd}"
            


