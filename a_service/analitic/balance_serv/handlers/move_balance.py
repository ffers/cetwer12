
from domain.models.balance_dto import BalanceDTO
from domain.models.move_balance_dto import MoveBalanceDTO
from domain.repositories.balance_repo import ItemRepository

class MoveBalance:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    '''
    я хочу считать баланс профита и витаскивать етот баланс когда он в наличии
    а он в наличии когда ми получаем очікувано и вичетаем тіло
    тоесть я би хотел иметь баланс зп и вичетать его отдельно чтоби понимать
    что ето четко баланс зп 
    я могу его пополнить вручную
    я би хотел чтоби он пополнялся автоматом и с него списивать
    вот мои мисли и спутались
    но в тот момент когда я буду снимать деньги ето незначит 
    что ми их уже заработали
    например можно вичесть то что висит на почте из зп и за вичетом етого 
    посути то что на почте ето просто проблема на две недели а бивает и на месец 
    тоесть нужно отслеживать заказ и только когда он в статусе виполнен 
    обрабативать его и тоесть наверноое может бить прикидочная аналитика
    и аналитика по факту
    на сегодняшний день пусть зотяби зп просто прибавляеться 
    в момент подсчета аналитики
    '''
    def update_balance_salary(self, move: MoveBalanceDTO):
        balance: BalanceDTO = self.repo.get(move.project_id)
        print(f'update_balance_salary {balance}')
        salary = balance.balance - move.sum
        return self.repo.update_balance(
            BalanceDTO(
                id=balance.id,
                balance=salary
            )
        )