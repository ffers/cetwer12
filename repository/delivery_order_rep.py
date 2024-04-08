from server_flask.db import db
from server_flask.models import DeliveryOrder

class DeliveryOrderRep:
    def add_item(self, order_id, status):
        item = DeliveryOrder(
            number_ttn="-",
            ref_ttn="-",
            number_registr="-",
            order_id=order_id,
            status_id=status
        )
        db.session.add(item)
        db.session.commit()
        db.session.close()
        return True

    def load_item(self, order_id):
        item = DeliveryOrder.query.filter_by(order_id=order_id).first()
        return item

    def update_ttn(self, order_id, data):
        order = self.load_item(order_id)
        if not order:
            self.add_item(order_id, 1)
            order = self.load_item(order_id)
        order.ref_ttn = data["ref_ttn"],
        order.number_ttn = data["number_ttn"]
        db.session.commit()
        db.session.close()
        return True

    def update_registr(self, items, data):
        for item in items:
            item = self.load_item(item)
            print(f"update registr {item}, {data}")
            item.ref_registr = data["ref_registr"]
            item.number_registr = data["number_registr"]
            db.session.commit()
        db.session.close()
        return True

    def reg_delete_in_item(self, items):
        for item in items:
            v = self.load_item(item)
            v.ref_registr = ''
            v.number_registr = ''
            db.session.commit()
        db.session.close()
        return True

    def load_item_filter_order(self, data):
        order_list = []
        print(data)
        for order_id in data:
            print(order_id)
            order = DeliveryOrder.query.filter_by(order_id=int(order_id)).first()
            order_list.append(order)
        return order_list





