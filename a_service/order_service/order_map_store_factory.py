




from abc import ABC, abstractmethod

from mapper import RozetkaMapper, promMapper
from a_service import ProductServ

class Mapper(ABC):
    def __init__(self, data_order, store_id):
        self.data_order = data_order
        self.store_id = store_id

    @abstractmethod
    def process(self):
        pass

class Rozetka(Mapper):
    def process(self):
        mapper = RozetkaMapper(ProductServ)
        return mapper.order(self.data_order, self.store_id)

class Prom(Mapper):
    def process(self):
        return promMapper(self.data_order, ProductServ, self.store_id)
         


class OrderMapStoreFactory:
    @staticmethod
    def factory(store_data, data):
        api = store_data.api
        apis = {
            "prom": Prom,
            "rozetka": Rozetka,
        }
        if api in apis:
            return apis[api](data, store_data.id)
        else:
            raise ValueError(f"Unknown api: {api}")