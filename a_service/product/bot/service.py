from .repository import ProductCounBot

pc_cl = ProductCounBot()

class BotProductSrv():
    def work_with_product(self, data):
        if "text" in data["message"]:
            text = data["message"]["text"]
            chat_id = data["message"]["chat"]["id"]
            print(text)
            update_color = pc_cl.manager_bot(text)
            return update_color
        else:
            return "Щось не те..."



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
