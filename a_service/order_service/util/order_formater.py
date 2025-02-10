from .formatters import Rozetka, Prom, Courier, Manager


class Formater:
    def __init__(self):
        self.strategies = {
            "prom": self.format_detailed,
            "rozetka": self.format_short,
            "courier": self.format_json,
            "manager": self.format_json
        }

    def format_order(self, order, format_type="manager"):
        if format_type in self.strategies:
            return self.strategies[format_type](order)
        raise ValueError(f"Unknown format type: {format_type}")

    def format_prom(self, order):
         return Prom.format(order)
    
    def format_rozetka(self, order):
         return Rozetka.format(order)
    
    def format_manager(self, order):
         return Manager.format(order)
    
    def format_courier(self, order):
         return Courier.format(order)
