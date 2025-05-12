

from abc import ABC, abstractmethod
from domain.models.crm_dto import CrmDTO

class ItemRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[CrmDTO]: pass

    @abstractmethod
    def get(self, item_id: int) -> CrmDTO: pass

    @abstractmethod
    def add(self, item: CrmDTO) -> None: pass

    @abstractmethod
    def update(self, item: CrmDTO) -> None: pass

    @abstractmethod
    def delete(self, item_id: int) -> None: pass
