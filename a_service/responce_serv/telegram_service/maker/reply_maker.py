
from ..parsers.parse_message import ParseMsgFactory
from flatten_dict import flatten


class Command:
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings

    def execute(self, pointer):
        return pointer  
    
class IfReply(Command): # парсинг текста
    def execute(self, pointer):
        text = ParseMsgFactory.factory("replytext", self.data, pointer)
        if text:
            return text
        return "Don`t have respone."
    
class Builder:
    def __init__(self):
        self.commands = []

    def add_command(self, command_class):
        self.commands.append(command_class)
        return self 

    def build(self, data, settings):
        pointer = None
        for cmd_class in self.commands:
            pointer = cmd_class(data, settings).execute(pointer)
            if not pointer:
                break
        return pointer


class ReplyDirector:
    def __init__(self):
        self.builder = Builder()

    def construct(self, data, settings):
        return (
            self.builder 
            .add_command(IfReply)
            .build(data, settings)
        )