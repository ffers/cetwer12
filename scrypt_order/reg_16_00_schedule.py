from black.telegram_controller import tg_cntrl
from black.order_cntrl import ord_cntrl
from black.delivery_order_cntrl import del_ord_cntrl
from server_flask.flask_app import flask_app
from utils import util_asx

OC_log = util_asx.oc_log("reg_16_00")

def reg_16_00():
    with flask_app.app_context():
        load_orders = ord_cntrl.load_confirmed_order()
        print(load_orders)
        list_dict = create_list_dict(load_orders)
        dict_order = del_ord_cntrl.add_registr(list_dict)
        tg_cntrl.sendPhoto()
        tg_cntrl.sendMessage(tg_cntrl.chat_id_np, dict_order["number_registr"])
        OC_log.info("Виконую завдання")

def create_list_dict(orders):
    list_dict = {"id": []}
    for order in orders:
        list_dict["id"].append(order.id)
    return list_dict


