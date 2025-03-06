
from ..parsers.parse_message import ParseMsgFactory
from flatten_dict import flatten

class Command:
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings

    def execute(self, pointer):
        return pointer  
    
class Type(Command):    # очень похоже на ifmessage но
    def execute(self, pointer):
        pointers = {
            "callback_query",
            "edited_message",
            "message", # при условии что message парсить команду
            }          # я нехочу передавать много данних
        return ParseMsgFactory.factory("type", self.data, pointers)

    
class TakeChat(Command):
    def execute(self, pointer):
        data = flatten(self.data, "dot")
        return ParseMsgFactory.factory("takechat", data, pointer)
    
class ChatName(Command):
    def execute(self, pointer):
        chats = self.settings.chats
        return ParseMsgFactory.factory("chatname", chats, pointer)
    
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
            if pointer == "Чат не зареєстровано":
                return pointer
        return pointer


class ChatDirector:
    def __init__(self):
        self.builder = Builder()

    def construct(self, data, settings):
        return (
            self.builder
            .add_command(Type)  
            .add_command(TakeChat)
            .add_command(ChatName)
            .build(data, settings)
        )