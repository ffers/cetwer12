from server_flask.db import db
from server_flask.models import DeliveryOrder

class DeliveryOrderRep:
    def add_item(self, data):
        item = DeliveryOrder(
            ref_ttn=data["ref_ttn"],
            number_ttn=data["number_ttn"],
            ref_registr=data["ref_registr"],
            number_registr=data["number_registr"],
            order_id=data["order_id"],
            status_id=data["status_id"]
        )
        db.session.add(item)
        db.session.commit()
        return item

    def load_item(self, order_id):
        item = DeliveryOrder.query.filter_by(order_id=order_id).first()
        return item

    def update_registr(self, items, data):
        for item in items:
            item = self.load_item(item)
            print(item)
            item.ref_registr = data["ref_registr"]
            item.number_registr = data["number_registr"]
            db.session.commit()
            return True

    def reg_delete_in_item(self, items):
        for item in items:
            v = self.load_item(item)
            v.ref_registr = ''
            v.number_registr = ''
            db.session.commit()
            return True

    def load_item_filter_order(self, data):
        order_list = []
        print(data)
        for order_id in data:
            print(order_id)
            order = DeliveryOrder.query.filter_by(order_id=int(order_id)).first()
            order_list.append(order)
        return order_list





