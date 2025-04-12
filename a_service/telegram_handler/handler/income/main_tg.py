from settings import Settings

from .maker import CommandDirector, ChatNameDirector, \
            TextDirector, ReplyDirector, ChatNummerDirector, AuthorDirector

from .group import CRM, Courier, Manager, Stock, \
            NPdelivery, ROZdelivery, UKRdelivery





class Resp:
    def __init__(self, data, chat_data):
        self.data = data
        self.chat_data = chat_data
        self.settings = Settings()

    def execute(self):
        pass

class ChatName(Resp):
    def execute(self):
        result = ChatNameDirector().construct(self.data, self.settings)
        self.chat_data.chat = result
        return result

class ChatNummer(Resp):
    def execute(self):
        result = ChatNummerDirector().construct(self.data, self.settings)
        self.chat_data.chat_nummer = result
        return result

class CommandHandler(Resp):
    def execute(self):
        result = CommandDirector().construct(self.data, self.settings)
        self.chat_data.cmd = result
        return result

class TextHandler(Resp):
    def execute(self):
        result = TextDirector().construct(self.data, self.settings)
        self.chat_data.text = result
        return result

class ReplyHandler(Resp):
    def execute(self):
        result = ReplyDirector().construct(self.data, self.settings)
        self.chat_data.reply = result
        return result

class AuthorHandler(Resp):
    def execute(self):
        result = AuthorDirector().construct(self.data, self.settings)
        self.chat_data.author = result
        print("devAuthorHandler:", result)
        print("self.chat_data.author:", self.chat_data.author)
        return result

class Group(Resp):
    def execute(self):
        chats = {
            "courier": Courier,
            "manager": Manager,
            # "crm": CRM,
            "stock": Stock,
            # "np_delivery": NPdelivery,
            # "roz_delivery": ROZdelivery,
            # "ukr_delivery": UKRdelivery,
        }
        if self.chat_data.chat in chats:
            return chats[self.chat_data.chat].factory(self.chat_data)
        return "Group responce: ok"
      
class Builder:
    def __init__(self):
        self.commands = [] 

    def add_command(self, command_class):
        self.commands.append(command_class)
        return self

    def build(self, data, data_chat): 
        pointer = None 
        for cmd_class in self.commands:
            pointer = cmd_class(data, data_chat).execute()
            print(pointer, "main_tg")
            if pointer == "just_message" or pointer == "unknown_chat":
                print("Останавливаем")
                return data_chat
        return data_chat

    
class Income: 
    def __init__(self):
        self.builder = Builder()

    def construct(self, data, data_chat):
        return (
            self.builder
            .add_command(ChatName)
            .add_command(ChatNummer)
            .add_command(CommandHandler)
            .add_command(TextHandler)
            .add_command(ReplyHandler)
            .add_command(AuthorHandler)
            .add_command(Group)
            .build(data, data_chat)
        )
