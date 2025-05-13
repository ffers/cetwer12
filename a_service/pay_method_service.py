from domain.models.pay_method_dto import PayMethodDTO


class PayMethodService:
    def __init__(self, repo):
        self.repo = repo

    def list_items(self):
        return self.repo.get_all()

    def get_item(self, item_id):
        return self.repo.get(item_id)
    
    def get_items_select(self):
        return self.repo.get_all_select()

    def create_item(self, name, description):
        
        self.repo.add(PayMethodDTO(name=name, description=description))

    def update_item(self, item_id, name, description):
        self.repo.update(
            PayMethodDTO(
                id=item_id, name=name, description=description
                )
            )

    def delete_item(self, item_id):
        self.repo.delete(item_id)
