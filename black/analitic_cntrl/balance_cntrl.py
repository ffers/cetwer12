

from a_service.analitic.balance_serv.balance_service import BalanceService
from domain.repositories.balance_repo import ItemRepository



class BalanceCntrl:
    def __init__(self, repo: ItemRepository):
        self.serv = BalanceService(repo)

    def move_balance(self, move):
        self.serv.move_balance(move)