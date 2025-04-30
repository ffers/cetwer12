


class StoreService:
    def __init__(self, repo):
        self.repo = repo

    def list_items(self):
        return self.repo.get_all()

    def get_item(self, item_id):
        return self.repo.get(item_id)
    
    def get_items_select(self):
        return self.repo.get_all_select()

    def create_item(self, name, api, token):
        from domain.models.store_dto import StoreDTO
        self.repo.add(StoreDTO(name=name, api=api, token=token))

    def update_item(self, item_id, name, api, token):
        from domain.models.store_dto import StoreDTO
        self.repo.update(
            StoreDTO(
                id=item_id, name=name, api=api, token=token
                )
            )

    def delete_item(self, item_id):
        self.repo.delete(item_id)
