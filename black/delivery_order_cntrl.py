from repository import DeliveryOrderRep, OrderRep
from a_service import DeliveryOrderServ
from api import NpClient

from utils import OC_logger

del_ord_serv = DeliveryOrderServ()
del_ord_rep = DeliveryOrderRep()
np_cl_api = NpClient()
ord_rep = OrderRep()


class DeliveryOrderCntrl:
    def __init__(self):
        self.logger = OC_logger.oc_log('black.deliv_order_cntrl')
    def add_registr(self, data):
        try:
            order_id_list = del_ord_serv.load_dict_order(data) # чистий ліст order_id з отриманного словаря
            orders = del_ord_rep.load_item_filter_order(order_id_list)  # лист об`єктів ордерів загружені по order_id
            list_ttn = del_ord_serv.create_list_ttn(orders) # створений список ref_ttn
            print(f"list_ttn  {list_ttn}")
            resp = np_cl_api.insertDocumentsReg(list_ttn) # запит в нп на ствоерня реєстру
            print(resp)
            dict_reg = {"number_registr": "Не вийшло створити перевірте підтвердженя НП"}
            if resp.get('success'):
                dict_reg = del_ord_serv.create_dict_reg(resp) # створення словаря на додавання в базу
                print(f"dict_reg {dict_reg}")
                bool = del_ord_rep.update_registr(order_id_list, dict_reg) #додано реф та номер реєстру в базу
                ord_rep.change_status_list(order_id_list, 11) #змінюємо статус на "очікує відправленя"
            raise ValueError('Відповідь НП: реєстр не створено')
        except Exception as e:
            print(f'DeliveryOrderCntrl: проблема')
            self.logger.error(f'DeliveryOrderCntrl: {e}')
            return {"number_registr": "Не вийшло створити перевірте підтвердженя НП"}

    def delete_ttn_in_reg(self, data):
        order_id_list = del_ord_serv.load_dict_order(data) # чистий ліст order_id з отриманного словаря
        orders = del_ord_rep.load_item_filter_order(order_id_list) # лист об`єктів ордерів загружені по order_id
        list_ttn = del_ord_serv.create_list_ttn(orders) # створений список ref_ttn
        print(list_ttn, orders[0].ref_registr)
        resp = np_cl_api.removeDocumentsReg(list_ttn, orders[0].ref_registr)
        print(resp)
        bool = False
        if resp["success"]:
            ord_rep.change_status_list(order_id_list, 2)
            bool = del_ord_rep.reg_delete_in_item(order_id_list)
        return bool

    def add_item(self, order_id, status):
        resp = del_ord_rep.add_item(order_id, status)
        return resp

    def update_item(self, first_data, order_id):
        dict_del_ord = del_ord_serv.create_dict(first_data, order_id)
        print(dict_del_ord)
        data_del_ord = del_ord_rep.update_ttn(order_id, dict_del_ord)
        return True


del_ord_cntrl = DeliveryOrderCntrl()






