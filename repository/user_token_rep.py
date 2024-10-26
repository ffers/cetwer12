from server_flask.db import db
from server_flask.models import UserToken

class UserTokenRep:
    def add_token(self):
        def add_product_source(self, data_list):
            try:
                item = UserToken(
                    article=data_list[0],
                    name=data_list[1],
                    price=data_list[2],
                    quantity=data_list[3],
                    money=data_list[4]
                )
                db.session.add(item)
                db.session.commit()
                db.session.close()
                return True
            except Exception as e:
                return False, e
