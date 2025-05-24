

from server_flask.models import DeliveryMethod as SQLItem
from domain.models.delivery_dto import DeliveryDTO
from domain.repositories.crm_repo import ItemRepository

class DeliveryRepositorySQLAlchemy(ItemRepository):
    def __init__(self, session=None):
        self.session = session

    def get_all(self):
        items = SQLItem.query.all()

        item_dtos = []
        for item in items:
            dto = DeliveryDTO(
                id=item.id,
                name=item.name
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
        return DeliveryDTO(
            i.id, i.name
            )

    def add(self, item: DeliveryDTO):
        sql_item = SQLItem(
            name=item.name
            )
        self.session.add(sql_item)
        self.session.commit()

    def update(self, item: DeliveryDTO):
        i = SQLItem.query.get_or_404(item.id)
        i.name = item.name
        self.session.commit()

    def delete(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        self.session.delete(i)
        self.session.commit()
