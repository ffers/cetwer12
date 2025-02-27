from ..telegram_service.main_tg import TGDirector

from settings import Settings

from .action_responce import ActionFactory
from .ready_responce import ReadyFactory

class Responce:
    def __init__(self, data, OrderCntrl, SourAnCntrl, TelegramCntrl):
        self.data = data
        self.OrderCntrl = OrderCntrl
        self.SourAnCntrl = SourAnCntrl
        self.TelegramCntrl = TelegramCntrl
        self.settings = Settings()

    def execute(self, pointer):
        return pointer

class IncomeResponce(Responce):  # Группи должни вернуть стандарт и команду с темой которой надо работать
    def execute(self, pointer):
        pointer = TGDirector().construct(self.data)
        print( "IncomeResponce")
        return pointer
    
class ActionResponce(Responce):  
    def execute(self, pointer):
        return ActionFactory.factory(pointer, self.OrderCntrl, self.SourAnCntrl)  
    
class TGResponce(Responce):  
    def execute(self, pointer):
        print(pointer, "ReadyResponce")
        resp = ReadyFactory.factory(pointer, 
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
            pointer = None
            for cmd_class in self.commands:
                pointer = cmd_class(data, OrderCntrl, SourAnCntrl, TelegramCntrl).execute(pointer)
                print(pointer, "Responce_step")
                if not pointer:
                    break
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
