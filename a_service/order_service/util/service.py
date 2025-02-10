

from datetime import datetime
from .order_formater import Formater


# Базовий клас замовлення
class Util:
    def __init__(self, order, format_type):
        self.order = order

    def process(self):
        raise NotImplementedError("Subclasses must implement process()")

# Класи для кожного статусу

class OrderFormater(Util):
    def process(self):
        text = Formater()
        text.format_order(self.order)
        return text

# Фабричний метод для створення замовлення за статусом
class UtilFactory:
    @staticmethod
    def factory(order, customer, format_type):
        factor = {
            "format": OrderFormater,
        }
        if format_type in factor:
            return factor[format_type](order, customer)
        else:
            raise ValueError(f"Unknown order status: {format_type}")