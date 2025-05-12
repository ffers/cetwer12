

from server_flask.models import Project as SQLItem
from domain.models.crm_dto import CrmDTO
from domain.repositories.crm_repo import ItemRepository

class CrmRepositorySQLAlchemy(ItemRepository):
    def __init__(self, session=None):
        self.session = session

    def get_all(self):
        stores = SQLItem.query.all()

        store_dtos = []
        for store in stores:
            dto = CrmDTO(
                id=store.id,
                name=store.name
            )
            store_dtos.append(dto)

        return store_dtos
    
    def get_all_select(self):
        stores = self.get_all() 
        store_select = []
        for store in stores:
            dto = {
                'id': store.id,
                'name': store.name,
            }
            store_select.append(dto)

        return store_select


    def get(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        return CrmDTO(
            i.id, i.name, i.timestamp, i.user_id
            )

    def add(self, item: CrmDTO):
        sql_item = SQLItem(
            name=item.name, 
            user_id=item.user_id
            )
        self.session.add(sql_item)
        self.session.commit()

    def update(self, item: CrmDTO):
        i = SQLItem.query.get_or_404(item.id)
        i.name = item.name
        self.session.commit()

    def delete(self, item_id):
        i = SQLItem.query.get_or_404(item_id)
        self.session.delete(i)
        self.session.commit()
