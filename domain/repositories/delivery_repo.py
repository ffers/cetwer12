

from abc import ABC, abstractmethod
from domain.models.delivery_dto import DeliveryDTO

class ItemRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[DeliveryDTO]: pass

    @abstractmethod
    def get(self, item_id: int) -> DeliveryDTO: pass

    @abstractmethod
    def add(self, item: DeliveryDTO) -> None: pass

    @abstractmethod
    def update(self, item: DeliveryDTO) -> None: pass

    @abstractmethod
    def delete(self, item_id: int) -> None: pass
