from decimal import Decimal

class CacheService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Ініціалізація кешу та інших потрібних параметрів
            cls._instance.cache = {}
        return cls._instance

    def set(self, key, value):
        self.cache[key] = value

    def get(self, key):
        return self.cache.get(key)

    def get_all(self):
        return self.cache.items()

    def format_float(self, num):
        try:
            if isinstance(num, int):
                num_format = str(f"{int(num)}.00")
                # Конвертуємо int у Decimal
                return Decimal(num_format)
            else:
                num_format = float(num)
                # Конвертуємо float у Decimal
                return Decimal(str(f"{num_format: .2f}"))
        except ValueError:
            return None

    def create_set(self, data):
        self.set("torg", data[0])
        self.set("body", data[1])
        self.set("workers", data[2])
        self.set("cpa", data[3])
        self.set("rozet", data[4])
        self.set("google", data[5])
        self.set("insta", data[6])
        self.set("profit", data[7])
        self.set("period", data[8])
        self.set("orders", data[9])
        print(f"кеш старт {self.get_all()}")


    def calculate_profit(self, revenue, cost_price):
        return revenue - cost_price

    def stock_func(self, items): # сток зависит от товара
        stock = 0
        if items:
            for item in items:
                stock += item.money
        self.set("stock", stock)
        return stock

    def income_func(self, item):
        income = 0
        if item:
            income += item.money
        self.set("income", income)
        return income

    def balance_func(self, balance_w):
        balance = 0
        income = self.get("income")
        if income:
            print(income)
            balance += income
            if balance_w:
                balance += balance_w.money
        self.set("balance", balance)
        return balance

    def wait_func(self): # вейт зависит от инком
        wait = self.get("torg") - self.get("income")
        self.set("wait", wait)
        print(f"Працює кеш {wait}")
        return wait

    def inwork_func(self): # зависит от всего в последнюю очередь
        inwork = self.get("wait") + self.get("stock")
        self.set("inwork", inwork)
        return inwork

    def salary_func(self):
        salary = self.get("profit") - self.get("workers") \
                 - self.get("cpa") - self.get("rozet") \
                 - self.get("google") - self.get("insta")
        self.set("salary", salary)
        return salary


    def qauntity_source(self, prod_source, sale_quantity):
        new_quantity = prod_source.quantity + sale_quantity
        self.set("quantity_source", new_quantity)
        return new_quantity



# # Використання
# cache = CacheService()
# cache.set('key1', 'value1')
#
# # В іншій частині програми
# cache = CacheService()
# print(cache.get('key1'))  # Виведе: value1
#
#
# # Використання

# revenue = 1000  # Виручка
# cost_price = 600  # Вартість закупки
# profit = cache.calculate_profit(revenue, cost_price)
# print("Прибуток:", profit)
