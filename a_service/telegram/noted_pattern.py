class Handler:
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler  # Позволяет связывать обработчики в цепочку

    def handle(self, data):
        if self.next_handler:
            return self.next_handler.handle(data)
        return None


import re

class TextCommandHandler(Handler):
    def handle(self, data):
        if "text" in data.get("message", {}):
            text = data["message"]["text"]
            print(text)
            return self.next_handler.handle(text) if self.next_handler else None
        return super().handle(data)

class ParseCommandHandler(Handler):
    def handle(self, text):
        if "#взял" in text or "#склад" in text:
            print("Обрабатываем склад...")
        if "35:" in text or "45:" in text:
            print("Парсим размер...")
            return self.next_handler.handle(text) if self.next_handler else None
        return super().handle(text)

class SizeCommandHandler(Handler):
    def handle(self, text):
        sizes = re.findall(r'(\d+х-*\d+)', text)
        data = {int(s.split('х')[0]): int(s.split('х')[1]) for s in sizes}
        print(f"Размеры: {data}")
        return data

class CommandFactory:
    @staticmethod
    def create_command():
        text_handler = TextCommandHandler()
        parse_handler = ParseCommandHandler()
        size_handler = SizeCommandHandler()

        text_handler.set_next(parse_handler).set_next(size_handler)
        return text_handler

class Command:
    def execute(self, data):
        pass

class ConfirmOrderCommand(Command):
    def execute(self, order_id):
        return ord_cntrl.confirmed_order(order_id)

class QuestionOrderCommand(Command):
    def execute(self, order_id):
        return ord_cntrl.question_order(order_id)


class ButtonCommandFactory:
    @staticmethod
    def create_command(data_keyb):
        commands = {
            "1": ConfirmOrderCommand,
            "2": QuestionOrderCommand
        }
        if data_keyb in commands:
            return commands[data_keyb]()
        return None

class FlagStrategy:
    @staticmethod
    def get_flag(text):
        flags = {
            "#взял": "#взял",
            "#склад": "#склад",
            "#редактируєм": "#склад"
        }
        return flags.get(text, None)

command_handler = CommandFactory.create_command()
command_handler.handle(data)  # Запускаем обработку текста

button_command = ButtonCommandFactory.create_command("1")
if button_command:
    button_command.execute(order_id)
