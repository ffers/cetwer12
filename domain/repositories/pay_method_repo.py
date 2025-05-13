

from abc import ABC, abstractmethod
from domain.models.pay_method_dto import PayMethodDTO

class ItemRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[PayMethodDTO]: pass

    @abstractmethod
    def get(self, item_id: int) -> PayMethodDTO: pass

    @abstractmethod
    def add(self, item: PayMethodDTO) -> None: pass

    @abstractmethod
    def update(self, item: PayMethodDTO) -> None: pass

    @abstractmethod
    def delete(self, item_id: int) -> None: pass
