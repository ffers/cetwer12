from settings import Settings
from ..parsers.parse_message import ParseMsgFactory
from ...command import Cmd_dict


class Command:
    def __init__(self, data, settings):
        self.data = data
        self.settings: Settings = settings

    def execute(self, pointer):
        return pointer  

class Type(Command):    # очень похоже на ifmessage но
    def execute(self, pointer):
        pointer =  ParseMsgFactory.factory("type", self.data, self.settings.handlers)
        return pointer
    
class IfReply(Command):
    def execute(self, pointer): 
        result = ParseMsgFactory.factory("replytext", self.data, self.settings.handlers)
        if result:
            return "reply_to_message"
        return pointer

class IfMessage(Command): # парсинг текста
    def execute(self, pointer):
        if "message" == pointer: 
            text = self.data.get("message", None).get("text", None)
            pointer =  ParseMsgFactory.factory("commandtext", Cmd_dict.command, text)
        return pointer
    
class Builder:
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)
        return self  # Позволяет использовать цепочку вызовов

    def build(self, data, settings):
        pointer = None  # Берем первый элемент (если есть)
        for cmd in self.commands:  # Проходим по остальным
            pointer = cmd(data, settings).execute(pointer)
            if not pointer:
                break
        return pointer

class CommandDirector:
    def __init__(self):
        self.builder = Builder()

    def construct(self, data, settings):
        return (
            self.builder
            .add_command(Type) 
            .add_command(IfReply)
            .add_command(IfMessage)
            .build(data, settings)
        )

# === Использование ===
# data = {
#     "message": {"chat": {"id": 12345}, "text": "#приход"}
# }
# pointer = "message"

# result = CommandPipelineFactory.execute(data, pointer)
# print(result)  # Должно вернуть "command1"


