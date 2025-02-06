from repository.color_bot_rep import ProductCounBot
from pydantic import BaseModel

class ColorDTO(BaseModel):
    size: int
    color_num: int
    quantity: int


class BotProductSrv():
    def __init__(self):
        self.pc_cl = ProductCounBot()

    def work_with_product(self, data):
        if "text" in data["message"]:
            text = data["message"]["text"]
            chat_id = data["message"]["chat"]["id"]
            print(text)
            update_color = self.pc_cl.manager_bot(text)
            return update_color
        else:
            return "Щось не те..."
         
    def make_int(self, data):
        new_data = {}
        for a, b in data.items():
            new_data.update({a: int(b)})
        return new_data
        
    def add_color(self, data):
        print(data)
        new_data = self.make_int(data)
        print(new_data)
        data_dto = ColorDTO.model_validate(new_data)
        return self.pc_cl.add_color(data_dto)

    def delete_color(self, id):
        return self.pc_cl.delete(id)
    
    # def add_quantity(self, text):
    #     try:
    #         if "35:" in text and "45:" in text:
    #             clean_35, clean_45 = self.crete_two(text)
    #             self.update_base(clean_35, "Colorrep35", flag)
    #             self.update_base(clean_45, "Colorrep45", flag)
    #         else:
    #             print(data)
    #             base, size = self.count_size(text)
    #             self.update_base(data, base, flag)
    #             print(f"ОСЬ ВИЙШЛО {data, flag, size}")
    #         create_response = self.actual_count()
    #         return create_response
    #     except:
    #         return "Неправильно сформульоване повідомлення"
    
    # def manager_bot(self, text):
    #     has_hashtag = "#взял" in text or "#склад" in text
    #     has_35 = "35:" in text
    #     has_45 = "45:" in text
    #     if not has_hashtag or not (has_35 or has_45):
    #         return "Неправильно сформульоване повідомлення"
    #     return self.add_quantity(text)
    
    # Chain of Responsibility
    class Handler:
        def __init__(self, next_handler=None):
            self.next_handler = next_handler
    
        def handle(self, text):
            if self.next_handler:
                return self.next_handler.handle(text)
            return "Команда не знайдена"
    
    class StartCommand(Handler):
        def handle(self, text):
            if text == "/start":
                return "Привіт! Я Telegram-бот."
            return super().handle(text)
    
    class HelpCommand(Handler):
        def handle(self, text):
            if text == "/help":
                return "Ось список доступних команд..."
            return super().handle(text)
    
    # Ланцюжок обробників
    # commands = StartCommand(HelpCommand())
    
    # print(commands.handle("/start"))  # Привіт! Я Telegram-бот.
    # print(commands.handle("/help"))   # Ось список доступних команд...
    # print(commands.handle("/unknown"))  # Команда не знайдена
        




