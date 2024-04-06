from repository import DeliveryOrderRep, OrderRep
from service_asx import DeliveryOrderServ
from api import NpClient

del_ord_serv = DeliveryOrderServ()
del_ord_rep = DeliveryOrderRep()
np_cl_api = NpClient()
ord_rep = OrderRep()


class DeliveryOrderCntrl:
    def add_registr(self, data):
        try:
            order_id_list = del_ord_serv.load_dict_order(data) # чистий ліст order_id з отриманного словаря
            orders = del_ord_rep.load_item_filter_order(order_id_list)  # лист об`єктів ордерів загружені по order_id
            list_ttn = del_ord_serv.create_list_ttn(orders) # створений список ref_ttn
            resp = np_cl_api.insertDocumentsReg(list_ttn) # запит в нп на ствоерня реєстру
            bool = False
            if resp["success"]:
                dict_reg = del_ord_serv.create_dict_reg(resp) # створення словаря на додавання в базу
                bool = del_ord_rep.update_registr(order_id_list, dict_reg) #додано реф та номер реєстру в базу
                ord_rep.change_status(order_id_list, 11) #змінюємо статус на "очікує відправленя"
            return bool
        except:
            return False

    def delete_ttn_in_reg(self, data):
        order_id_list = del_ord_serv.load_dict_order(data) # чистий ліст order_id з отриманного словаря
        orders = del_ord_rep.load_item_filter_order(order_id_list) # лист об`єктів ордерів загружені по order_id
        list_ttn = del_ord_serv.create_list_ttn(orders) # створений список ref_ttn
        print(list_ttn, orders[0].ref_registr)
        resp = np_cl_api.removeDocumentsReg(list_ttn, orders[0].ref_registr)
        bool = False
        if resp["success"]:
            ord_rep.change_status(order_id_list, 2)
            bool = del_ord_rep.reg_delete_in_item(order_id_list)
        return bool


    # def add_list_ref(self, data):
    #     list_ref = []
    #     for item in data:
    #         order = del_ord_rep.load_item(item)
    #         if data:
    #             list_ref.append(order.ref_ttn)
    #             print(list_ref)
    #         else:
    #             print(f"Нема ттн для ")
    #     return list_ref






