

from abc import ABC, abstractmethod
from domain.models.balance_dto import BalanceDTO

class ItemRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[BalanceDTO]: pass

    @abstractmethod
    def get(self, item_id: int) -> BalanceDTO: pass

    @abstractmethod
    def get_project_id(self, item_id: int) -> BalanceDTO: pass

    @abstractmethod
    def add(self, item: BalanceDTO) -> None: pass

    @abstractmethod
    def update(self, item: BalanceDTO) -> None: pass

    @abstractmethod
    def update_balance(self, item: BalanceDTO) -> None: pass

    @abstractmethod
    def update_wait(self, item: BalanceDTO) -> None: pass

    @abstractmethod
    def update_stock(self, item: BalanceDTO) -> None: pass

    @abstractmethod
    def update_inwork(self, item: BalanceDTO) -> None: pass

    @abstractmethod
    def delete(self, item_id: int) -> None: pass
