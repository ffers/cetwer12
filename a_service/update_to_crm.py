import os
from server_flask.db import db
# from black import tg_cntrl
from repository import ord_rep

class UpdateToCrm():
    def __init__(self):
        self.change_data = None
        self.order_id = None
        pass

    def manager(self, data):
        flag = data["flag"]
        self.order_id = data["order_id"]
        if "change" in data:
            self.change_data = data["change"]
        self.db_order(self.order_id, flag)
        return self.order_id

    def db_order(self, order_id, flag):
        try:
            print(f"ПОЧАЛОСЬ update {order_id}")
            order = ord_rep.load_for_code(order_id)
            self.change_order(order, flag)
            db.session.commit()
            db.session.close()
            print(f"ЗАКІНЧИВСЯ update {order_id}")
            return order_id
        except:
            pass
            # tg_cntrl.sendMessage(tg_cntrl.chat_id_info, f"️❗️❗️❗️ НЕ ВИЙШЛО ОНОВИТИ замовлення {order_id} В CRM сторона CRM")

    def change_order(self, order, flag):
        print(f"flag {flag}")
        if flag == "canceled":
            order.ordered_status_id = 5
        elif flag == "paid":
            order.prompay_status_id = 1
            order.ordered_status_id = 3
        elif flag == "unpaid":
            order.prompay_status_id = 2
            order.ordered_status_id = 4
        elif flag == "refunded":
            order.ordered_status_id = 5
            order.prompay_status_id = 3

up_to_srm = UpdateToCrm()


