from abc import ABC, abstractmethod
from domain.models.store_dto import StoreDTO

class ItemRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[StoreDTO]: pass

    @abstractmethod
    def get(self, item_id: int) -> StoreDTO: pass

    @abstractmethod
    def get_token(self, item_token: str) -> StoreDTO: pass

    @abstractmethod
    def add(self, item: StoreDTO) -> None: pass

    @abstractmethod
    def update(self, item: StoreDTO) -> None: pass

    @abstractmethod
    def delete(self, item_id: int) -> None: pass
