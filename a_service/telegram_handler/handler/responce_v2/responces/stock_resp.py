
from utils import handle_error
from ..base import Command


class StockResp(Command):
    def execute(self, data_chat):
        if data_chat.content:
            data_chat = self.text_report_add(data_chat)
            resp = self.tg.sendMessage(self.tg.chat_id_courier, data_chat.text)
            return f"додано Ярік {resp}"
        else:
            self.tg.sendMessage(self.tg.chat_id_courier, "Неправильно сформульоване повідомлення")
        return data_chat 
    
    def text_report_add(self, pointer):
        try:  
            # if not pointer.comment:
            #     raise
            for item in pointer.content:
                pointer.text += "{}: {}\n".format(
                    item["article"], 
                    item["quantity"]
                    )
            return pointer 
        except Exception as e:
            handle_error(e, "parse_responce text report")
            pointer.text = "От халепа незнаю що віповісти"
            return pointer  