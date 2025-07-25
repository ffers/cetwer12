

from server_flask.models import Balance as SQLItem
from domain.models.balance_dto import BalanceDTO
from domain.repositories.balance_repo import ItemRepository
from sqlalchemy.orm import Session

class BalanceRepositorySQLAlchemy(ItemRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        items = SQLItem.query.all()

        item_dtos = []
        for item in items:
            dto = BalanceDTO(
                id=item.id,
                balance=item.balance,
                wait=item.wait,
                stock=item.stock,
                inwork=item.inwork
            )
            item_dtos.append(dto)

        return item_dtos
    
    def get_all_select(self):
        items = self.get_all() 
        item_select = []
        for item in items:
            dto = {
                'id': item.id,
                'balance': item.balance,
            }
            item_select.append(dto)

        return item_select


    def get(self, item_id):
        i = SQLItem.query.get(item_id)
        if not i: i = self.add_new()
        return BalanceDTO(
            i.id, i.project_id, i.balance, i.wait, i.stock, i.inwork
            )

    def get_project_id(self, item_id):
        i = SQLItem.query.filter_by(project_id=item_id).one_or_none()
        if not i: i = self.add_new(item_id)
        return BalanceDTO(
            i.id, i.project_id, i.balance, i.wait, i.stock, i.inwork
            )


    def add(self, item: BalanceDTO):
        sql_item = SQLItem(
            balance=item.balance, 
            wait=item.wait,
            stock=item.stock,
            inwork=item.inwork
            )
        self.session.add(sql_item)
        self.session.commit()

    def add_new(self, project_id):
        item = SQLItem(
            project_id=project_id,
            balance=0.00, 
            wait=0.00,
            stock=0.00,
            inwork=0.00
            )
        self.session.add(item)
        self.session.commit()
        return self.get_project_id(project_id)


    def update(self, item: BalanceDTO):
        i = SQLItem.query.get_or_404(item.id)
        i.balance=item.balance, 
        i.wait=item.wait,
        i.stock=item.stock,
        i.inwork=item.inwork
        self.session.commit()
        return 

    def update_balance(self, item: BalanceDTO):
        try:
            i = SQLItem.query.get_or_404(item.id)
            i.balance = item.balance
            self.session.commit()
            self.session.refresh(i) # моожет ошибка кбудет непомню
            return i
        except Exception as e:
            print(e)
            raise ValueError('update_balance repo dont work')
        

    def update_wait(self, item: BalanceDTO):
        i = SQLItem.query.get_or_404(item.id)
        i.wait = item.wait
        self.session.commit()
        return self.get(item.id)

    def update_stock(self, item: BalanceDTO):
        i = SQLItem.query.get_or_404(item.id)
        i.stock = item.stock
        self.session.commit()

    def update_inwork(self, item: BalanceDTO):
        i = SQLItem.query.get(item.id)
        i.inwork = item.inwork
        print('update_inwork:', i.inwork)
        self.session.commit()
        e = self.get(item.id)
        print('update_inwork:', e.inwork)

    def delete(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        self.session.delete(i)
        self.session.commit()
