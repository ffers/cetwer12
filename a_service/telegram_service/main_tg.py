from settings import Settings

from .maker import CommandDirector, ChatDirector, \
            TextDirector, ReplyDirector

from .group import CRM, Courier, Manager, Stock, \
            NPdelivery, ROZdelivery, UKRdelivery

from dataclasses import dataclass

@dataclass
class ChatData:
    chat: str = None
    cmd: str = None
    text: str = None
    reply: str = None
    content: list = None
    resp: list = None
    comment: str = None

class Resp:
    def __init__(self, data):
        self.data = data
        self.settings = Settings()

    def execute(self, pointer):
        return pointer

class ChatHandler(Resp):
    def execute(self, chat_data: ChatData):
        result = ChatDirector().construct(self.data, self.settings)
        chat_data.chat = result
        return result

class CommandHandler(Resp):
    def execute(self, chat_data: ChatData):
        result = CommandDirector().construct(self.data, self.settings)
        chat_data.cmd = result
        return result

class TextHandler(Resp):
    def execute(self, chat_data: ChatData):
        result = TextDirector().construct(self.data, self.settings)
        chat_data.text = result
        return result

class ReplyHandler(Resp):
    def execute(self, chat_data: ChatData):
        result = ReplyDirector().construct(self.data, self.settings)
        chat_data.reply_text = result
        return True

# class ChatCmd(TG):  
#     def execute(self, pointer):
#         chat = ChatDirector().construct(self.data, self.settings)
#         cmd = CommandDirector().construct(self.data, self.settings)
#         text = TextDirector().construct(self.data, self.settings)
#         reply_text = ReplyDirector().construct(self.data, self.settings)
#         pointer = chat, cmd, text, reply_text
#         return pointer  
    
# class ChatFactory:
#     @staticmethod
#     def build_chat_data(data, settings):
#         chat_data = ChatData()
        
#         for handler_cls in [ChatHandler, CommandHandler, TextHandler, ReplyHandler]:
#             handler = handler_cls()
#             if handler.execute(data, settings, chat_data) is None:
#                 print(f"❌ Процесс отменен: {handler_cls.__name__} вернул None")
#                 return None  # Отменяем процесс

#         return chat_data  # Все успешно


class Group(Resp):
    def execute(self, data: ChatData):
        chats = {
            "courier": Courier.factory(data),
            "manager": Manager.factory(data),
            # "crm": CRM.factory(cmd),
            "stock": Stock.factory(data),
            # "np_delivery": NPdelivery.factory(cmd),
            # "roz_delivery": ROZdelivery.factory(cmd),
            # "ukr_delivery": UKRdelivery.factory(cmd),
        }
        chat_data = chats.get(data.chat, None)
        print(chat_data.content, "Group")
        return chat_data

      
class Builder:
    def __init__(self):
        self.commands = []

    def add_command(self, command_class):
        self.commands.append(command_class)
        return self

    def build(self, data):
        try:   
            data_chat = ChatData
            for cmd_class in self.commands:
                pointer = cmd_class(data).execute(data_chat)
                print(pointer, "main_tg")
                if not pointer:
                    break
            return data_chat
        except:
            return None
    
class TGDirector:
    def __init__(self):
        self.builder = Builder()

    def construct(self, data):
        return (
            self.builder
            .add_command(ChatHandler)
            .add_command(CommandHandler)
            .add_command(TextHandler)
            .add_command(ReplyHandler)
            .add_command(Group)
            .build(data)
        )
