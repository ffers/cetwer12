


from ..base import Order


class ConfirmedOrder(Order):
    def process(self): # треба виконати шагі підвердження та додати підпис
        print(f"Підтверджено {self.order_id}")
        return {"confirmed": "ok"}


