from settings import Settings
from ..parsers.parse_message import ParseMsgFactory
from ...command import CmdDict


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
    
class CheckCommand(Command):
    def execute(self, pointer): 
        return ParseMsgFactory.factory("request", self.data, self.settings.handlers)
        

class IfMessage(Command): # парсинг текста
    def execute(self, pointer):
        if "message.text" == pointer:
            text = self.data.get("message", None).get("text", None)
            if text:             
                pointer = ParseMsgFactory.factory("commandtext", CmdDict.command, text)
        
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
                print("Command not found!")
                break
        return pointer

class CommandDirector:
    def __init__(self):
        self.builder = Builder()

    def construct(self, data, settings):
        return (
            self.builder
            .add_command(Type) 
            .add_command(CheckCommand)
            .add_command(IfMessage)
            .build(data, settings)
        )




