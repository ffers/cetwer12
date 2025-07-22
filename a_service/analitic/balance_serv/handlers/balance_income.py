
from domain.models.balance_dto import BalanceDTO
from domain.repositories.balance_repo import ItemRepository

class BalanceIncome:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    def count(self, description, sum):
        pass