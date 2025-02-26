from ..parsers.parse_text import ParseText
from ..parsers.parse_message import ParseMsgFactory

class Command:
    def __init__(self, T: ParseText, M: ParseMsgFactory):
        self.text_p = T()
        self.msg_p = M()

    def execute(self, chat_data):
        pass

class MsgCommand(Command):
    def execute(self, chat_data):
        pass
        
class ArrivalCommand(Command):
    def execute(self, chat_data):
        data = self.text_p.parse_colon(chat_data) #парсим 
        print(data.content, "ArrivalCommand")
        #добавляєм на склад
        #возвращаєм результат
        return data

class CommandHandler:
    @staticmethod
    def factory(chat_data):
        commands = {

            "stock": ArrivalCommand,

        } 
        if chat_data.cmd in commands:
            return commands[chat_data.cmd](
                ParseText, ParseMsgFactory
                ).execute(chat_data)
        return f"Немає команди {chat_data.cmd}"
            


