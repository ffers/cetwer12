


class TgAnswerSerw:
    def id_message(self, resp):
        id_message_int = resp["result"]["message_id"]
        id_chat_int = resp["result"]["chat"]["id"]
        return id_message_int, id_chat_int




# Заказ-дубликат
# Не получается дозвониться