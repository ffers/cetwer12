
from repository  import CostumerRep, RecipientRep
from dataclasses import dataclass

@dataclass
class Data:
    first_name: str = None
    last_name: str = None
    second_name: str = None
    phone: str = None
    email: str = None

class ClientServ:
    def __init__(self, Repo):
        self.repo = Repo()

    def parser_from_order(self, order):
        item = Data()
        item.firs_tname = order.client_firstname
        item.last_name = order.client_lastname
        item.second_name = order.client_surname
        item.phone = order.phone
        item.email = order.email
        return item
    
    def execute(self, order):
        item = self.parser_from_order(order)
        return self.repo.create(item)
    
class ClientBuilder:
    def __init__(self):
        self.commands = [
            ClientServ(CostumerRep),
            ClientServ(RecipientRep)
        ]


    def build(self, order):
        pointer = None
        for cmd_class in self.commands:
            pointer = cmd_class.execute(order)
            if not pointer:
                break
        return pointer

