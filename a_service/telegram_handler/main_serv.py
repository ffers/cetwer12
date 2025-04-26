from dataclasses import dataclass
from .handler import Income, Action, ResponceFactory
from mapper import TextOrderManager

from settings import Settings

"""
чтоби добавить новую команду
В command надо прописать новую команду 
В group изменить команду соответвующую чату если нет команди то остановится виполнение
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
    author: str = None

class Worker: 
    def __init__(self, data, **deps):
        self.data = data
        self.OrderCntrl = deps["OrderCntrl"]
        self.SourAnCntrl = deps["SourAnCntrl"]
        self.TelegramCntrl = deps["TelegramCntrl"]
        self.order_serv = deps["OrderServ"]
        self.settings = Settings()
        deps["TextFormat"] = TextOrderManager
        self.deps = deps


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
        return Action.factory(pointer, **self.deps)  
    
class TGResponce(Worker):  
    def execute(self, pointer):
        resp = ResponceFactory.factory(pointer, 
                    **self.deps)
        return pointer  

class Builder:
    def __init__(self):
        self.commands = []

    def add_command(self, command_class):
        self.commands.append(command_class)
        return self

    def build(self, data, **deps):
        # try:   
            pointer = ChatData()
            tg = deps["TelegramCntrl"]()
            for cmd_class in self.commands:
                pointer = cmd_class(data, **deps).execute(pointer)
                print("Працює: ", cmd_class.__name__)
                if not pointer:
                    print("Невиконано!: ", cmd_class.__name__)
                    tg.sendMessage(-421982888, "dev Невиконано!: ", cmd_class.__name__)
                    return pointer
                if pointer.chat == "unknown_chat":
                    print("Невідомий чат")
                    return pointer
            return pointer
        # except Exception as e:
        #     return f"Не працює main_serv: {str(e)}"
    
class ResponceDirector:
    def __init__(self):
        self.builder = Builder()

    def construct(self, 
                  data, 
                  **deps):
        return (
            self.builder
            .add_command(IncomeResponce)
            .add_command(ActionResponce)
            .add_command(TGResponce)
            .build(data, **deps)
        )
