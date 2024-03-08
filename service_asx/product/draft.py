#
# def await_tg_button(self, data): # black
#     dsr_cl.await_tg_button(data)
#
# def await_tg_button(self, data): # dispatcher
#     dsr_cl.await_tg_button(data)
# def await_tg_button(self, data):
#     resp = button_hand(data)
#     return resp
#
#
# def button_hand():
#     if "message" in data_in:
#         search_reply_message(data_in) # add rozet ttn
#         aw_cl.await_telegram(data_in)
#     return '', 200


# def await_telegram(data):
#     if "text" in data["message"]:
#         print("Отримав повідомленя в тексті")
#         if "entities" in data["message"]:
#             dsr_cl.parse(data)
#         chat_id = data["message"]["chat"]["id"]
#         print(chat_id)
#         print(ch_id_sk)
#         if int(ch_id_sk) == chat_id:
#             print("Отримали повідомлення з Робочого чату")
#             dsr_cl.work_with_product(data)
#
#
# def parse(self, data_in):
#     command = data_in["message"]["entities"][0]["type"]
#     if "bot_command" in command:
#         print("Отримав команду боту")
#         mreg_cl.manage_reg(data_in)
#
#
# def work_with_product(self, data):
#     text = data["message"]["text"]
#     chat_id = data["message"]["chat"]["id"]
#     print(text)
#     update_color = pc_cl.manager_bot(text)
#     tg_cl.send_message_f(chat_id, update_color)
