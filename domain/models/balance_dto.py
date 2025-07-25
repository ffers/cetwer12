

from dataclasses import dataclass
from datetime import datetime

from decimal import Decimal

@dataclass
class BalanceDTO:
    id: int = None
    project_id: int = None
    balance: Decimal = Decimal('0.00')
    wait: Decimal = Decimal('0.00')
    stock: Decimal = Decimal('0.00')
    inwork: Decimal = Decimal('0.00')
    salary: Decimal = Decimal('0.00')
    rozetka_pay: Decimal = Decimal('0.00')
    nova_pay: Decimal = Decimal('0.00')

