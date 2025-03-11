from dataclasses import dataclass
from .construct import Income, Action, ResponceFactory

from settings import Settings

"""
чтоби добавить новую команду
В command надо прописать новую команду 
В group прописать команду соответвующую чату если нет команди то остановить виполнение
В екшен добавить действие прописать возможно парсер 
В респонс подготовить ответ для тг если необходим

"""
@dataclass
class ChatData:
    chat: str = None
    chat_nummer: str = None
    cmd: str = None
    text: str = None 
    reply: str = None
    content: list = None
    resp: list = None
    comment: str = None

class Worker: 
    def __init__(self, data, OrderCntrl, SourAnCntrl, TelegramCntrl):
        self.data = data
        self.OrderCntrl = OrderCntrl
        self.SourAnCntrl = SourAnCntrl
        self.TelegramCntrl = TelegramCntrl
        self.settings = Settings()

    def execute(self, pointer):
        return pointer 
 
class IncomeResponce(Worker):  # Группи должни вернуть стандарт и команду с темой которой надо работать
    def execute(self, pointer):
        pointer = Income().construct(self.data, pointer) 
        # print(
        #     "{}\n{}\n{}\n{}\n{}\n{}\n{}\n".format( 
        #         pointer.chat,
        #         pointer.cmd,
        #         pointer.text,
        #         pointer.reply,
        #         pointer.content,
        #         pointer.resp, 
        #         pointer.comment,
        #     )
        # )
        return pointer
    
class ActionResponce(Worker):  
    def execute(self, pointer):
        return Action.factory(pointer, self.OrderCntrl, self.SourAnCntrl)  
    
class TGResponce(Worker):  
    def execute(self, pointer):
        resp = ResponceFactory.factory(pointer, 
                    self.OrderCntrl, self.SourAnCntrl, self.TelegramCntrl)
        return pointer  

class Builder:
    def __init__(self):
        self.commands = []

    def add_command(self, command_class):
        self.commands.append(command_class)
        return self

    def build(self, data, OrderCntrl, SourAnCntrl, TelegramCntrl):
        # try:   
            pointer = ChatData()
            for cmd_class in self.commands:
                pointer = cmd_class(data, OrderCntrl, SourAnCntrl, TelegramCntrl).execute(pointer)
                print("Працює: ", cmd_class.__name__)
                if not pointer:
                    print("Невиконано!: ", cmd_class.__name__)
                    TelegramCntrl().sendMessage(-421982888, "dev Невиконано!: ", cmd_class.__name__)
                    return pointer
                if pointer.chat == "unknown_chat":
                    print("Невідомий чат")
                    return pointer
            return pointer
        # except:
        #     return "Не працює responce_serv"
    
class ResponceDirector:
    def __init__(self):
        self.builder = Builder()

    def construct(self, data, OrderCntrl, SourAnCntrl, TelegramCntrl):
        return (
            self.builder
            .add_command(IncomeResponce)
            .add_command(ActionResponce)
            .add_command(TGResponce)
            .build(data, OrderCntrl, SourAnCntrl, TelegramCntrl)
        )
