
from .base import OrderContext
import re


class AddOrder:
    def __init__(self, ctx: OrderContext):
        self.ctx = ctx

    def add_quantity_orders_costumer(self, phone):
        digits = re.sub(r'\D', '', phone)
        if digits.startswith('380') and len(digits) == 12:
            digits = '0' + digits[3:]
        print(f'add_quantity_orders_costumer: {digits}')
        orders = self.ctx.order_repo.search_for_all(digits)
        if not orders:
            return 1
        return len(orders) + 1
        