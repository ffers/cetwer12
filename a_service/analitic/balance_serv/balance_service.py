
from domain.models.balance_dto import BalanceDTO
from domain.models.move_balance_dto import MoveBalanceDTO

from domain.repositories.balance_repo import ItemRepository
from .handlers.move_balance import MoveBalance


class BalanceService:
    def __init__(self, repo: ItemRepository):
        self.repo = repo
        self.move = MoveBalance(self.repo)

    def list_items(self):
        return self.repo.get_all()

    def get_item(self, item_id):
        return self.repo.get(item_id)
    
    def get_items_select(self):
        return self.repo.get_all_select()

    def create_item(self, balance, wait, stock, inwork):
        self.repo.add(BalanceDTO(
            balance=balance, 
            wait=wait,
            stock=stock,
            inwork=inwork
            ))

    def update_item(self, item_id, balance, wait, stock, inwork):
        self.repo.update(
            BalanceDTO(
                id=item_id, 
                balance=balance, 
                wait=wait,
                stock=stock,
                inwork=inwork
                )
            )

    def delete_item(self, item_id):
        self.repo.delete(item_id)
 
    def move_balance(self, move_dto: MoveBalanceDTO):
        '''
        проблема в том что нужно записать баланс в общий журнал но ето нельзя
        сдклать потомучто журнал завязан только под товар
        сделаем журнал денег
        на половину журнал готов но пока его пропустим
        '''
        balance = self.move.update_balance_salary(move_dto)
        print(balance)
        return balance
    

   
