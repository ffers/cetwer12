class ContextHandler:
    def __init__(self, api, telegram, repo):
        self.api = api
        self.telegram = telegram
        self.repo = repo

class Handler:
    def __init__(self, context):
        self.ctx = context

class GetOrderPending(Handler):
     def execute(self, orders):
        pass


class OrderHandler:
    def __init__(self):
        self.commands = []

    def add_command(self, command_class):
        self.commands.append(command_class)
        return self

    def build(self, context):
        orders = []
        for cmd_class in self.commands:
            orders.extend(cmd_class(context).execute(orders))
            print(orders, "builder")
        return orders

def get_orders(self):
        orders = []
        statuses = ("pending", "paid")
        for status in statuses:
            orders.extend(self.load_orders(status)) 
        return orders