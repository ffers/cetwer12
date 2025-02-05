from black.telegram_controller import tg_cntrl
from black.order_cntrl import OrderCntrl
from black.delivery_order_cntrl import del_ord_cntrl
from server_flask.flask_app import flask_app
from utils import util_asx
from asx.black.analitic_cntrl.sour_an_cntrl import SourAnCntrl
from black.telegram_cntrl.tg_cash_cntrl import TgCashCntrl
from black import SourDiffAnCntrl
from utils import SendRequest
import time

class RegSchedulleSrv():
    def __init__(self):
        self.OC_log = util_asx.oc_log("reg_16_00")
        self.sour = SourAnCntrl()
        self.ord = OrderCntrl()
        self.quan_stok = TgCashCntrl()
        self.sour_diff_cntrl = SourDiffAnCntrl()
        self.send_req = SendRequest()

    def reg_17_00(self):
            try: # реквест визиває апі а потім апі визиває функціі
                black_pic = self.sendTgBlackPic()
                dict_order = self.createReg()
                self.OC_log.info(dict_order)
                self.sendTg(dict_order)
                self.OC_log.info("Виконую завдання")
                return True
            except Exception as e:
                info = f"Невийшло створити реєстр {e}"
                self.OC_log(info)
                tg_cntrl.sendMessage(tg_cntrl.chat_id_info, info)
                return False

    def createReg(self):
        load_orders = self.ord.load_confirmed_order()
        print(load_orders)
        list_dict = self.create_list_dict(load_orders)
        print(list_dict)
        dict_order = del_ord_cntrl.add_registr(list_dict)
        return dict_order

    def sendTgBlackPic(self):
        id_photo = 'AgACAgIAAxkBAAIMl2YWFuaONHD9_7SWvzDiiK8vmNQSAAK31jEbGsoISBKbThvzHGUpAQADAgADbQADNAQ'
        resp_photo = tg_cntrl.sendPhoto(id_photo)
        if not resp_photo:
            self.OC_log.info("Телеграм не дал ответа Photo")
        self.OC_log.info(resp_photo)
        return True

    def sendTg(self, dict_order):
        resp_message = tg_cntrl.sendMessage(tg_cntrl.chat_id_np, dict_order["number_registr"])
        if not resp_message:
            self.OC_log.info("Телеграм не дал ответа Месседж")
        return True


    def create_list_dict(self, orders):
        list_dict = {"id": []}
        for order in orders:
            list_dict["id"].append(order.id)
        return list_dict

    def reg_20_00(self): 
            self.ord.change_status_roz()
            self.sour.add_quantity_crm_today()
            time.sleep(1)
            self.sour.sort_analitic("all")
            self.sour.sort_analitic("year")
            self.sour.sort_analitic("month")
            self.sour.sort_analitic("week")
            self.sour.sort_analitic("day")
            self.quan_stok.quan_f("#quan 35N, 45N, 35W1, 45W1, 35N10, 40N10, 45N10, BX1, BX2, BX3, BX4, BX5, 35N11, 40N11, 45N11, 35W, 45W, 35W13, 45W13") 
            # запустить програму скидивания наличия
            print("Успіх")
            # изменить статус розетки
            # провести аналитику
            return True
        
    def reg_20_01(self):
            return self.sour.sour_diff_all_source_sold("two_days") 


    def reg_16_58(self):
            self.sour.sort_analitic("all")
            self.sour.sort_analitic("year")
            self.sour.sort_analitic("month")
            self.sour.sort_analitic("week")
            self.sour.sort_analitic("day")
            print("Успіх")
            return True
        
    def reg_17_00_new(self):
        data = None
        url = "http://localhost:8000/v2/orders/16_58"
        self.send_req.send_http_json(data, url)




