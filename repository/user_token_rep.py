from server_flask.db import db
from server_flask.models import UserToken
from DTO import UserTokenDTO
import os


class UserTokenRep(object):
    def __init__(self, token):
        if token == token: # на будущее проверка доступа через Fast
            print("Authorizate")
        else:
            print("Unathorithate")
   
    def add_token(self, d: UserTokenDTO):
        try:
            item = UserToken(d)  
            db.session.add(item)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            return False, str(e)
        
    def update_token(self, d: UserTokenDTO):
        try:
            item = UserToken.query.filter_by(user_id=d.user_id).first()
            item.update_from_dto(d)  
            db.session.commit() 
            return True
        except Exception as e:
            db.session.rollback() 
            return False, str(e) 
        
    def load_token_checkbox(self, user_id):
        token = UserToken.query.filter_by(user_id=user_id).first()
        return token.checkbox_access_token


        


