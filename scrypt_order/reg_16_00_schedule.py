from black.telegram_controller import tg_cntrl
from black.order_cntrl import OrderCntrl
from black.delivery_order_cntrl import del_ord_cntrl
from server_flask.flask_app import flask_app
from utils import util_asx
from black.sour_an_cntrl import SourAnCntrl

class RegSchedulleSrv():
    def __init__(self):
        self.OC_log = util_asx.oc_log("reg_16_00")
        self.sour = SourAnCntrl()
        self.ord = OrderCntrl()

    def reg_16_00(self):
        with flask_app.app_context():
            load_orders = self.ord.load_confirmed_order()
            print(load_orders)
            list_dict = self.create_list_dict(load_orders)
            dict_order = del_ord_cntrl.add_registr(list_dict)
            id_photo = 'AgACAgIAAxkBAAIMl2YWFuaONHD9_7SWvzDiiK8vmNQSAAK31jEbGsoISBKbThvzHGUpAQADAgADbQADNAQ'
            resp = tg_cntrl.sendPhoto(id_photo)
            self.OC_log.info(resp)
            tg_cntrl.sendMessage(tg_cntrl.chat_id_np, dict_order["number_registr"])
            self.OC_log.info("Виконую завдання")

    def create_list_dict(self, orders):
        list_dict = {"id": []}
        for order in orders:
            list_dict["id"].append(order.id)
        return list_dict

    def reg_20_00(self):
        with flask_app.app_context():
            self.ord.change_status_roz()
            self.sour.sort_analitic("all")
            self.sour.sort_analitic("day")
            self.sour.sort_analitic("week")
            self.sour.sort_analitic("month")
            self.sour.sort_analitic("year")
            print("Успіх")
            # изменить статус розетки
            # провести аналитику

