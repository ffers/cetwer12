
from server_flask.models import SourceDifference
from server_flask.db import db
from sqlalchemy import desc
import copy


  

class SourDiffAnRep():
    def __init__(self) -> None:
        pass

    def load_source_difference(self):
        product = SourceDifference.query.all() #.query.order_by(ProductDifference.timestamp.desc()).all 
        return product
    
    def load_source_diff_line(self, id):
        line = SourceDifference.query.get_or_404(id)
        return line
  
    def add_source_difference(self, body):
        # try:
            add = SourceDifference(event_date=body[0], 
                                   source_id=body[1],
                                   quantity_crm=body[2],
                                   quantity_stock=body[3],
                                   difference=body[4]
                                   )
            db.session.add(add)
            db.session.commit() 
        #     return True
        # except:
        #     return False  
         
    def update_source_difference(self, *args):
        try:
            item = SourceDifference.query.filter_by(product_id=args[0]).first()
            item.quantity_crm = args[1]
            item.quantity_stock = args[2]
            db.session.commit()
            return True
        except:
            return False
         
  
    def load_source_difference_id_period(self, id, start, stop):
        product = SourceDifference.query.filter(
            SourceDifference.event_date >= start,
            SourceDifference.event_date <= stop,
            SourceDifference.source_id == id
        ).order_by(desc(SourceDifference.timestamp)).all()
        return product
         
    def add_quantity_crm(self, body):
        # try:
            add = SourceDifference(
                event_date=body[0], 
                source_id=body[1],
                quantity_crm=body[2]
                                   )
            db.session.add(add)
            db.session.commit() 
        #     return True
        # except:
        #     return False


    def update_source_diff_line(self, args, id):
        try:
            item = SourceDifference.query.get_or_404(id)
            item.quantity_crm = args[0]
            item.quantity_stock = args[1]
            db.session.commit()
            return True
        except:
            return False
    
    def update_source_diff_line_sold(self, quantity, id):
        try:
            item = SourceDifference.query.get_or_404(id)
            item.sold = quantity
            db.session.commit()
            return True
        except:
            return False
          
    def update_diff_sum(self, quantity, id):
        try:
            item = SourceDifference.query.get_or_404(id)
            item.difference = quantity
            db.session.commit()
            return True
        except:
            return False
       
               
    def update_diff_table(self, data):
        try:
            for row in data:
                item = self.load_source_diff_line(row[0])
                item.quantity_stock = row[1]
                db.session.commit()
            return True
        except:
            return False
        
    def delete_diff_line(self, id):
        try:
            item = self.load_source_diff_line(id)
            item_copy = copy.deepcopy(item)
            print(item_copy.source_id, "item_copy")
            db.session.delete(item)
            db.session.commit()
            return True, item_copy.source_id
        except:
            return False