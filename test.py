import uuid
import random

def generate_order_code(prefix='ASX'):
    digits = [random.choice('0123456789') for _ in range(6)]
    unique_id = ''.join(digits) # Генеруємо унікальний ID та беремо перші 6 символів
    order_code = f'{prefix}-{unique_id}'
    return order_code

# Приклад використання
order_code1 = generate_order_code()
print(order_code1)

order_code2 = generate_order_code()
print(order_code2)