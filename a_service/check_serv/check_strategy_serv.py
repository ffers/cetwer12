from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute(self, data):
        pass

class OnlineMode(Strategy):
    def execute(self, data):
        return f"Виконані дії: {data}"

class OfflineMode(Strategy):
    def execute(self, data):
        return f"Відповідь в ТГ: {data}"

# Контекст, що використовує стратегії
class Context:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def do_action(self, data):
        return self.strategy.execute(data)

# Використання:
# data = "user_data"

# context = Context(GetElements())
# print(context.do_action(data))

# context.set_strategy(ActionElements())
# print(context.do_action(data))

# context.set_strategy(ResponseElements())
# print(context.do_action(data))
