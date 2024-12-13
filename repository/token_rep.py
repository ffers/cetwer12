from server_flask.db import db
from server_flask.models import UserToken


class TokenRep:
    def add_token(self, data_list):
        try:
            item = UserToken(
                project=data_list[0],
                user_id=data_list[1]
            )
            db.session.add(item)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            return False, e
        


