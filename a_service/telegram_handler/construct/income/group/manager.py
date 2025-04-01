from ..parsers.parse_text import ParseText


class Command:
    def __init__(self, PT: ParseText):
        self.text_parse = PT()


    def execute(self, chat_data):
        pass
          
class NewOrders(Command):
    def execute(self, chat_data):
        return chat_data
    
class AddComment(Command):
    def execute(self, chat_data):
        if "Замовлення №" in chat_data.reply:
            chat_data.cmd = "reply_manager"
            chat_data.comment = chat_data.text
            chat_data.text = self.text_parse.search_order_code(chat_data.reply)
            return chat_data
        return chat_data
    
class SearchOrder(Command):
    def execute(self, chat_data):
        chat_data.cmd = "search_order_manager"
        chat_data.text = self.text_parse.search_6_number(chat_data.text)
        return chat_data

    
# 🔹 Клас, що виконує команду 
class CommandHandler:
    @staticmethod
    def factory(chat_data):
        commands = {
            "new_orders": NewOrders,
            "reply_to_message": AddComment,
            "search_order": SearchOrder
        } 
        if chat_data.cmd in commands:
            return commands[chat_data.cmd](
                ParseText
                ).execute(chat_data)
        return f"Немає команди {chat_data.cmd}"
            



