from ..parsers.parse_message import ParseMsgFactory


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

class TakeText(Command):
    def execute(self, pointer):
        return ParseMsgFactory.factory("taketext", self.data, pointer)
    
class TextBuilder:
    def __init__(self):
        self.commands = []

    def add_command(self, command_class):
        self.commands.append(command_class)
        return self

    def build(self, data, settings):
        pointer = None
        for cmd_class in self.commands:
            pointer = cmd_class(data, settings).execute(pointer)
            print(pointer, "text_maker")
        return pointer

class TextDirector:
    def __init__(self):
        self.builder = TextBuilder()

    def construct(self, data, settings):
        return (
            self.builder
            .add_command(Type)  
            .add_command(TakeText)
            .build(data, settings)
        )