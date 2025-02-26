from ..parsers.parse_text import ParseText
from ..parsers.parse_message import ParseMsgFactory

class Command:
    def __init__(self, T: ParseText, M: ParseMsgFactory):
        self.text_p = T()
        self.msg_p = M()

    def execute(self, content, markup):
        pass


# 🔹 Telegram-команди
class MsgCommand(Command):
    def execute(self, content, markup):
        pass
        
    
class ArrivalCommand(Command):
    def execute(self, content, murkup):
        data = self.text_p.parse_colon(content) #парсим 
        print(data)
        #добавляєм на склад
        #возвращаєм результат
        return "Привіт! Я добавляю на склад"
    
class TakeCommand(Command):
    def execute(self):
        #парсим 
        #убавляєм на складе
        #возвращаєм результат
        return "Привіт! Я віднімаю з склада"




        return None

# 🔹 Клас, що виконує команду
class CommandHandler:
    @staticmethod
    def factory(chat_data):
        commands = {
            # "take": "take",
            # "stock": "stock",
            # "edit": "edit",
            "arrival": ArrivalCommand,
            # "comment":"comment"
        } 
        if chat_data.cmd in commands:
            return commands[chat_data.cmd](
                ParseText, ParseMsgFactory
                ).execute(chat_data)
        return f"Немає команди {chat_data.cmd}"
            


