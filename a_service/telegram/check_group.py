# CHAT_ID_INFO=196584706
# CHAT_ID_CONFIRMATION=196584706
# CHAT_ID_HELPER=196584706
# CH_ID_NP=196584706
# CH_ID_SK=196584706
# CH_ID_UKR=196584706
# CH_ID_ROZ=196584706
# CH_ID_CASH=196584706
# CH_ID_SHOP=196584706
# CH_ID_CORECTOR=-616047623

class State:
    def handle(self, bot, text):
        pass

class StartState(State):
    def handle(self, bot, text):
        if text == "/start":
            bot.state = WaitingForInputState()  # Переходимо в інший стан
            return "Введіть ваше ім'я:"
        return "Невідома команда"

class WaitingForInputState(State):
    def handle(self, bot, text):
        bot.state = StartState()  # Повертаємось до початкового стану
        return f"Дякую, {text}!"

class Bot:
    def __init__(self):
        self.state = StartState()

    def handle(self, text):
        return self.state.handle(self, text)

# bot = Bot()
# print(bot.handle("/start"))  # Введіть ваше ім'я:
# print(bot.handle("Олексій"))  # Дякую, Олексій!