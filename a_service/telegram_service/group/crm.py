class Command:
    def execute(self):
        pass

# 🔹 Telegram-команди
class ArrivalCommand(Command):
    def execute(self):
        return "Привіт! Я добавляю на склад"
    
class TakeCommand(Command):
    def execute(self):
        return "Привіт! Я віднімаю з склада"

# 🔹 Фабрика команд
class CommandFactory:
    TELEGRAM_COMMANDS = {}  #{ "/start": StartCommand  }

    CUSTOM_COMMANDS = {
        "#взял": TakeCommand,
        "#прихід": ArrivalCommand
    }

    @classmethod
    def get_command(cls, text):
        text = text.lower()

        # Перевіряємо Telegram-команди
        if text in cls.TELEGRAM_COMMANDS:
            return cls.TELEGRAM_COMMANDS[text]()

        # Перевіряємо кастомні команди (шукаємо в тексті)
        for command, command_class in cls.CUSTOM_COMMANDS.items():
            if command in text:
                return command_class()

        return None

# 🔹 Клас, що виконує команду
class CommandHandler:
    def handle_command(self, text):
        command = CommandFactory.get_command(text)
        return command.execute() if command else "Команда не знайдена"
# 🔹 Використанняhandler = CommandHandler()print(handler.handle_command("/start"))  # Привіт! Я Telegram-бот.print(handler.handle_command("Щось написав #взял"))  # Обробка команди 'взял'.print(handler.handle_command("Невідома команда"))  # Команда не знайдена