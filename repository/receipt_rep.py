from server_flask.db import db
from datetime import datetime, timedelta
from sqlalchemy import func
from server_flask.models import Receipt, Shift
from DTO import ReceiptDTO, ShiftDTO


class ReceiptRep:
    def add(self, d: ReceiptDTO):
        try:
            item = Receipt(d) 
            db.session.add(item)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            return False, str(e) 

    def update(self):
        pass

    def delete(self):
        pass


class ShiftRep:
    def add(self, d: ShiftDTO):
        try:
            item = Shift(d) 
            db.session.add(item)
            db.session.commit()
            db.session.close()
            return True
        except Exception as e:
            return False, str(e) 
    
    def update(self):
        pass

    def delete(self):
        pass
        
    def load_shift_date(self, date):
        token = Shift.query.filter_by(timestamp=date).first()
        return token.checkbox_access_token
