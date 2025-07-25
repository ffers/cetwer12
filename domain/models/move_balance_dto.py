

from dataclasses import dataclass
from datetime import datetime

from decimal import Decimal

@dataclass
class MoveBalanceDTO:
    project_id: int = None
    sum: Decimal = Decimal('0.00')
    description: str = None