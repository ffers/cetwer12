from decimal import Decimal

def format_float(num): # str float або int
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

print(format_float("10.00"))