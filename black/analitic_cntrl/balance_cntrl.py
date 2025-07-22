

from a_service.analitic.balance_serv.balance_service import BalanceService
from domain.repositories.balance_repo import ItemRepository



class BalanceCntrl:
    def __init__(self, repo: ItemRepository):
        self.balance = BalanceService(repo)

    def add_income_balance(self, description, sum):
        self.add_income_balance(description, sum)