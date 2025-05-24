
from domain.models.delivery_dto import DeliveryDTO

class DeliveryService:
    def __init__(self, repo):
        self.repo = repo

    def list_items(self):
        return self.repo.get_all()

    def get_item(self, item_id):
        return self.repo.get(item_id)
    
    def get_items_select(self):
        return self.repo.get_all_select()

    def create_item(self, name):
        self.repo.add(DeliveryDTO(name=name))

    def update_item(self, item_id, name):
        self.repo.update(
            DeliveryDTO(
                id=item_id, name=name
                )
            )

    def delete_item(self, item_id):
        self.repo.delete(item_id)
