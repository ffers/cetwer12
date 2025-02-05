from repository.color_bot_rep import ProductCounBot
from pydantic import BaseModel

class ColorDTO(BaseModel):
    size: int
    color_num: int
    quantity: int


class BotProductSrv():
    def __init__(self)      :
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



# {'update_id': 677781446, 'message': {'message_id': 5237,
#                                      'from': {'id': 196584706, 'is_bot': False, 'first_name': 'Denys',
#                                               'username': 'fferses', 'language_code': 'uk'},
#                                      'chat': {'id': 196584706, 'first_name': 'Denys', 'username': 'fferses',
#                                               'type': 'private'}, 'date': 1724321039, 'photo': [
#         {'file_id': 'AgACAgIAAxkBAAIUdWbHDQ9988wxqxW0YzkifoaBSoxpAAK31jEbGsoISBKbThvzHGUpAQADAgADcwADNQQ',
#          'file_unique_id': 'AQADt9YxGxrKCEh4', 'file_size': 338, 'width': 67, 'height': 90},
#         {'file_id': 'AgACAgIAAxkBAAIUdWbHDQ9988wxqxW0YzkifoaBSoxpAAK31jEbGsoISBKbThvzHGUpAQADAgADbQADNQQ',
#          'file_unique_id': 'AQADt9YxGxrKCEhy', 'file_size': 1928, 'width': 240, 'height': 320},
#         {'file_id': 'AgACAgIAAxkBAAIUdWbHDQ9988wxqxW0YzkifoaBSoxpAAK31jEbGsoISBKbThvzHGUpAQADAgADeAADNQQ',
#          'file_unique_id': 'AQADt9YxGxrKCEh9', 'file_size': 7036, 'width': 600, 'height': 800},
#         {'file_id': 'AgACAgIAAxkBAAIUdWbHDQ9988wxqxW0YzkifoaBSoxpAAK31jEbGsoISBKbThvzHGUpAQADAgADeQADNQQ',
#          'file_unique_id': 'AQADt9YxGxrKCEh-', 'file_size': 11879, 'width': 960, 'height': 1280}]}}
