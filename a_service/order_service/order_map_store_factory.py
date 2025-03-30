




from abc import ABC, abstractmethod

from mapper import RozetkaMapper
from a_service import ProductServ

class Mapper(ABC):
    def __init__(self, data_order):
        self.data_order = data_order

    @abstractmethod
    def process(self):
        pass

class Rozetka(Mapper):
    def process(self):
        mapper = RozetkaMapper(ProductServ)
        return mapper.order(self.data_order)

class Prom(Mapper):
    def process(self):
        pass


class OrderMapStoreFactory:
    @staticmethod
    def factory(cmd, data):
        cmds = {
            "prom": Prom,
            "rozetka": Rozetka,
        }
        if cmd in cmds:
            return cmds[cmd](data)
        else:
            raise ValueError(f"Unknown api: {cmd}")