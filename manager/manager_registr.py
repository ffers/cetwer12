# from api.nova_poshta.create_data import RegistrDoc
# from telegram import TgClient
# import os
#
#
# tg_cl = TgClient()
# reg_cl = RegistrDoc()
#
# CHAT_INFO = os.getenv("chat_id_info")
#
#
# class ManageReg():
#     def register(self):
#         resp = reg_cl.create_reg()
#         resp_error_ttn = resp["data"][0]["Data"]["Errors"]
#         resp_error = resp["data"][0]["Errors"]
#
#         if resp_error or resp_error_ttn:
#             tg_cl.send_message_f(CHAT_INFO, f"Реєстр не створено: {resp_error_ttn} {resp_error}")
#         else:
#             reg_number = resp["data"][0]["Number"]
#             reg_cl.save_reg(resp)
#             reg_cl.delete_doc()
#             tg_cl.send_message_f(CHAT_INFO, f"Номер реєстру: {reg_number}")
#             tg_cl.send_message_f(CHAT_INFO, resp_error)
#
#     def addregister(self):
#         resp = reg_cl.add_reg()
#         resp_error_ttn = resp["data"][0]["Data"]["Errors"]
#         resp_error = resp["data"][0]["Errors"]
#         if resp_error or resp_error_ttn:
#             tg_cl.send_message_f(CHAT_INFO, f"В Реєстр не додані накладні: {resp_error_ttn} {resp_error}")
#         else:
#             reg_number = resp["data"][0]["Number"]
#             reg_cl.delete_doc()
#             tg_cl.send_message_f(CHAT_INFO, f"Додано в: {reg_number}")
#             tg_cl.send_message_f(CHAT_INFO, resp_error)
#
#     def deleteregister(self):
#         resp = reg_cl.deleteReg()
#         if resp["success"] == False:
#             resp_error = resp["errors"][0]
#             tg_cl.send_message_f(CHAT_INFO, f"Реєстр не росформовано: {resp_error}")
#         else:
#             tg_cl.send_message_f(CHAT_INFO, f"Росформовано реєстр: {resp}")
#
#
#     def manage_reg(self, data):
#         text = data["message"]["text"]
#
#         if "/register" in text:
#             print("Створити реєстр")
#             self.register()
#
#         if "/addregister" in text:
#             print("Додати в реєстр")
#             self.addregister()
#
#         if "/deleteregister" in text:
#             print("Видалити реєстр")
#             self.deleteregister()
