from server_flask.models import Recipient
from server_flask.db import db



class RecipientRep:
    def create(self, item_new):
        item = Recipient(
            firs_tname=item_new.firs_tname,
            last_name=item_new.last_name,
            second_name=item_new.second_name,
            phone=item_new.phone,
            email=item_new.email
        )
        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)
        return item

    def read_item(self, item_id):
        item = Recipient.query.get_or_404(item_id)

    def update(self, item_id, item_new):
        item = self.read_item(item_id)
        item.firs_tname=item_new.first_name,
        item.last_name=item_new.last_name,
        item.second_name=item_new.second_name,
        item.phone=item_new.phone,
        item.email=item_new.email
        db.session.commit()
        db.session.refresh(item)
        return item

    def delete(self, item_id):
        item = self.read_item(item_id)
        db.session.delete(item)
        db.session.commit()
        return True



    def read_all(self):
        items = Recipient.query.all()
        return items
    