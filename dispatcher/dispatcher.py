# from manager import ManageReg
# from service_asx.order import ManagerTg
# from service_asx.delivery import ManagerTTN
# from telegram import TgClient
# # from helper_crm import PromToCrm, UpdateToCrm
# # from helper_crm.crm_to_telegram import CrmToTelegram
#
#
# # crmtotg_cl = CrmToTelegram()
# # crm_cl = PromToCrm()
# # upd_crm = UpdateToCrm()
# # pc_cl = ProductCounBot()
# tg_cl = TgClient()
# mng_cl = ManagerTTN()
# mreg_cl = ManageReg()
# tgmn_cl = ManagerTg()
#
# class Dispatcher():
#     def create_ttn(self, order_id):
#         ttn_data = mng_cl.create_ttn(order_id)
#         resp_ok = mng_cl.add_ttn_crm(order_id, ttn_data)
#         return ttn_data
#
#     # def parse(self, data_in):
#     #     command = data_in["message"]["entities"][0]["type"]
#     #     if "bot_command" in command:
#     #         print("Отримав команду боту")
#     #         mreg_cl.manage_reg(data_in)
#
#     # def send_order(self, data, flag=None):
#     #     print(f"ДИвимось флаг {flag}")
#     #     resp = None
#     #     if flag == "prom_to_crm":
#     #         data_for_tg = crmtotg_cl.manger(data)
#     #         resp = crm_cl.add_order(data, data_for_tg)
#     #     if flag == "update_to_crm":
#     #         resp = upd_crm.manager(data)
#     #     else:
#     #         tgmn_cl.see_flag(data, flag)
#     #     return resp
#
#         # передаєм для відправки телеграм
#
#     # def create_ttn_cab(self, order):
#     #     resp = mng_cl.create_ttn_cabinet(order)
#     #     return resp
#
#     # def work_with_product(self, data):
#     #     text = data["message"]["text"]
#     #     chat_id = data["message"]["chat"]["id"]
#     #     print(text)
#     #     update_color = pc_cl.manager_bot(text)
#     #     tg_cl.send_message_f(chat_id, update_color)
#
#
#
#
#
#
#
#
#
#
#
#
#
