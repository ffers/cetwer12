
from ..parsers.parse_message import ParseMsgFactory
from flatten_dict import flatten

class Command:
    def __init__(self, data, settings):
        self.data = data
        self.settings = settings

    def execute(self, pointer):
        return pointer  

    
class Type(Command):
    def execute(self, pointer):
        return ParseMsgFactory.factory("request", self.data, self.settings.handlers)
    
class Author(Command):
    def execute(self, pointer):
        if pointer == "reply_to_message":
            return ParseMsgFactory.factory("takeauthor", self.data, self.settings.handlers)
    
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
        return pointer


class AuthorDirector:
    def __init__(self):
        self.builder = Builder()

    def construct(self, data, settings):
        return (
            self.builder
            .add_command(Type)
            .add_command(Author)
            .build(data, settings)
        )