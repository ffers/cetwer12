
from repository  import CostumerRep, RecipientRep, OrderRep
from dataclasses import dataclass


@dataclass
class DataOrder:
    costumer_id: int = None
    recipient_id: int = None



@dataclass
class DataClient:
    first_name: str = None
    last_name: str = None
    second_name: str = None
    phone: str = None
    email: str = None

class WriteClient:
    def parser_from_order(self, order):
        item = DataClient()
        item.first_name = order.client_firstname
        item.last_name = order.client_lastname
        item.second_name = order.client_surname
        item.phone = order.phone
        item.email = order.email
        return item
    
    def execute(self, order, Repo): ### послед
        item = self.parser_from_order(order)
        return Repo().create(item)
    
class WriteOrderID:
    def execute(self, order, Repo, data): ### послед
        return Repo().update_new_dataclass(order.id, data)
    

class Handler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, order, context: DataOrder):
        result = self.process(order, context)
        if result and self.next_handler:
            return self.next_handler.handle(order, context)
        return result

    def process(self, order, context):
        raise NotImplementedError("Override process() in subclass")

# 1. Запис у Costumer
class SaveCustomer(Handler):
    def process(self, order, context):
        item = WriteClient().execute(order, CostumerRep)
        context.costumer_id = item.id
        print(f"✅ Костюмер збережено з ID {item.id}")
        return True

# 3. Запис у Recipient
class SaveRecipient(Handler):
    def process(self, order, context):
        item = WriteClient().execute(order, RecipientRep)
        context.recipient_id = item.id
        print(f"✅ Отримувач збережено з ID {item.id}")
        return True

# 4. Запис ID у Order (Recipient)
class SaveIDToOrder(Handler):
    def process(self, order, context):
        repo = OrderRep()
        result = repo.update_new_dataclass(order.id, context)
        text = f"✅ ID ресіпієнта {result.recipient_id} та \n"
        text += f"✅ ID costumer {result.costumer_id} записано в ордер"
        print(text)
        return True

# Емуляція замовлення
class Order:
    def __init__(self):
        self.customer_id = None
        self.recipient_id = None

# Побудова ланцюжка команд
class OrderProcessingPipeline:
    def __init__(self):
        self.pipeline = SaveCustomer(
                SaveRecipient(
                    SaveIDToOrder()
                )
        )

    def process(self, order):
        result = self.pipeline.handle(order, DataOrder)
        print("\nРезультат виконання:", "✅ Успішно" if result else "❌ Помилка")
        return result


    def change_order(self, orders):
        for order in orders:
            resp = self.create_client(order)
            if not resp:
                break
        return resp


    def create_client(self, order):
        resp = "without answer"
        # try: 
        resp = OrderProcessingPipeline().process(order)
        if not resp:
            raise
        return resp
        # except:
        #     print("create_client:", resp)
        #     return False



