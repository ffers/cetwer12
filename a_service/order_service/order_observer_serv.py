


class Observer:
    def update(self, order):
        pass

class OrderFormatter:
    @staticmethod
    def format_order(order):
        items_text = "\n".join(
            f"{item.quantity}x {item.product} - {item.price}$"
            for item in order.items
        )
        return (
            f"🛒 Order #{order.order_id}\n"
        f"👤 Customer: {order.customer}\n"
        f"📦 Status: {order.status}\n"
        f"🛍 Items:\n{items_text}\n"
        f"💰 Total: {order.get_total_price()}$\n"
        f"💳 Payment: {order.payment_status}\n"
        f"🚚 Delivery: {order.delivery_method}\n"
        f"📨 Recipient: {order.recipient_name}, {order.recipient_phone}"
        )
class AddOrder(Observer):
    def update(self, order):
        print(f"CRM: Order {order.order_dto.id} addet to base")

class EmailNotifier(Observer):
    def update(self, order):
        print(f"Email: Order {order.order_dto} changed to {order.status}")

class InventoryUpdater(Observer):
    def update(self, order):
        print(f"Inventory: Updating stock for Order {order.order_dto}")

class TelegramConfirm(Observer):
    def update(self, order):
        text = OrderFormatter.format_order(order)
        print(f"Telegram: Sending sms for client {text}")
    
class ReceiptNotifer(Observer):
    def update(self, order):
        print(f"Receipt: Видано чек на замовлення: {order.order_dto}, {order.receipt}")

class Order:
    def __init__(self, order_dto):
        self.order_dto = order_dto
        self.status = None
        self.receipt = None
        self.order = None
        self.observers = []
        self._default_observers()

    def _default_observers(self):
        self.add_observer(EmailNotifier())
        self.add_observer(InventoryUpdater())
        self.add_observer(TelegramConfirm())
        
    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def update_status(self, status):
        self.status = status
        self.notify_observers()

    def get_receipt(self, receipt):
        self.add_observer(ReceiptNotifer())
        self.receipt = receipt


