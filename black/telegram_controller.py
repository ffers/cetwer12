import os
from dotenv import load_dotenv
from service_asx.order import search_reply_message, button_hand
from service_asx import BotProductSrv

pr_bt_srv = BotProductSrv()


env_path = '../common_asx/.env'
load_dotenv(dotenv_path=env_path)

chat_id_helper = os.getenv("CHAT_ID_HELPER") # вп: -421982888; розет: -1001822083358; укр: -1001173544690; нп: -1001391714237
chat_id_np = "-1001391714237"
chat_id_ukr = "-1001173544690"
chat_id_rozet = "-1001822083358"
chat_id_vp = os.getenv("CHAT_ID_INFO")
ch_id_sk = os.getenv("CH_ID_SK")


class TelegramController():
    def await_telegram(self, data):
        if "text" in data["message"]:
            print("Отримав повідомленя в тексті")
            if "entities" in data["message"]:
                command = data["message"]["entities"][0]["type"]
                if "bot_command" in command:
                    print("Отримав команду боту")


        chat_id = data["message"]["chat"]["id"]
        print(chat_id)
        print(ch_id_sk)
        if int(ch_id_sk) == chat_id:
            print("Отримали повідомлення з Робочого чату")
            pr_bt_srv.work_with_product(data)

    def await_tg_button(self, data):
        if "message" in data:
            search_reply_message(data)
            self.await_telegram(data)
        if "callback_query" in data:
            button_hand(data)
        return '', 200