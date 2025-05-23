
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class AnaliticDto:
    id: int = None
    torg: Decimal = Decimal('0.00')
    body: Decimal = Decimal('0.00')
    worker: Decimal = Decimal('0.00')
    prom: Decimal = Decimal('0.00')
    rozet: Decimal = Decimal('0.00')
    google: Decimal = Decimal('0.00')
    insta: Decimal = Decimal('0.00')
    profit: Decimal = Decimal('0.00')
    salary: Decimal = Decimal('0.00')
    inwork: Decimal = Decimal('0.00')
    stock: Decimal = Decimal('0.00')
    balance: Decimal = Decimal('0.00')
    wait: Decimal = Decimal('0.00')
    income: Decimal = Decimal('0.00')
    wait: Decimal = Decimal('0.00')
    period: str = ''
    orders: int = 0