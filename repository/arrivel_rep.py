from server_flask.db import db
from server_flask.models import Arrival

class ArrivalRep:
    def add_arrival(self, combined_list):

        for item in combined_list:
            datetime_new, product_id, quantity, price, total = item
            arrival = Arrival(product_id=product_id, body_price=price, quantity=quantity,
                                             total_price=total, datetime_new=datetime_new)
            db.session.add(arrival)
        db.session.commit()
        return True

    def load_arrival(self):
        arrival = Arrival.query.order_by(Arrival.timestamp).all()
        return arrival