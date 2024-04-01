import random

class OrderServ:
    def generate_order_code(self, prefix='ASX'):
        digits = [random.choice('0123456789') for _ in range(6)]
        unique_id = ''.join(digits)  # Генеруємо унікальний ID та беремо перші 6 символів
        order_code = f'{prefix}-{unique_id}'
        return order_code

    def examine_code(self, order, code):
        while True:
              # Генеруємо нове значення
            if new_digits not in order:  # Перевіряємо, чи таке значення ще не використовувалось
                used_values.add(new_digits)  # Додаємо нове значення до множини використаних
                return new_digits  # Повертаємо унікальне значення





