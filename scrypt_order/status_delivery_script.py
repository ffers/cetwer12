from api import NpClient
from repository import OrderRep, DeliveryOrderRep
from service_asx import DeliveryOrderServ
from server_flask.flask_app import flask_app

np_cl_api = NpClient()
ord_rep = OrderRep()
del_ord_serv = DeliveryOrderServ()
del_ord_rep = DeliveryOrderRep()

class StatDelScript:
    def load_track(self):
        with flask_app.app_context():
            try:
                order_registred = ord_rep.load_registred()
                list_ref = del_ord_serv.create_list_for_orders(order_registred)
                print(list_ref)
                if list_ref:
                    resp = np_cl_api.trackingDocument(list_ref)
                    self.checking(resp)
            except:
                pass

    def checking(self, resp):
        print(f"checking {resp}")
        for order in resp["data"]:
            number_ttn = order["Number"]
            print(number_ttn)
            if order["StatusCode"] == "5":
                order_del = del_ord_rep.load_order_for_ref(number_ttn)
                ord_rep.change_status_list([order_del.order_id], 8)





