

from server_flask.models import PaymentMethod as SQLItem
from domain.models.pay_method_dto import PayMethodDTO
from domain.repositories.pay_method_repo import ItemRepository

class PayMethodRepositorySQLAlchemy(ItemRepository):
    def __init__(self, session=None):
        self.session = session

    def get_all(self):
        items = SQLItem.query.all()

        item_dtos = []
        for item in items:
            dto = PayMethodDTO(
                id=item.id,
                name=item.name,
                description=item.description
            )
            item_dtos.append(dto)

        return item_dtos
    
    def get_all_select(self):
        items = self.get_all() 
        item_select = []
        for item in items:
            dto = {
                'id': item.id,
                'name': item.name,
            }
            item_select.append(dto)

        return item_select


    def get(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        return PayMethodDTO(
            i.id, i.name, i.description
            )

    def add(self, item: PayMethodDTO):
        sql_item = SQLItem(
            name=item.name, 
            description=item.description
            )
        self.session.add(sql_item)
        self.session.commit()

    def update(self, item: PayMethodDTO):
        i = SQLItem.query.get_or_404(item.id)
        i.name = item.name
        i.description = item.description
        self.session.commit()

    def delete(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        self.session.delete(i)
        self.session.commit()
