
from domain.models.crm_dto import CrmDTO

class CrmService:
    def __init__(self, repo):
        self.repo = repo

    def list_items(self):
        return self.repo.get_all()

    def get_item(self, item_id):
        return self.repo.get(item_id)
    
    def get_items_select(self):
        return self.repo.get_all_select()

    def create_item(self, name, user_id):
        self.repo.add(CrmDTO(name=name, user_id=user_id))

    def update_item(self, item_id, name):
        self.repo.update(
            CrmDTO(
                id=item_id, name=name
                )
            )

    def delete_item(self, item_id):
        self.repo.delete(item_id)
