from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class MoneyJournalDto(BaseModel):
    id: Optional[int] = None
    timestamp: Optional[datetime] = None
    event_date: Optional[datetime]
    description: Optional[str]
    movement: Decimal
    total: Decimal

    model_config = {
        "from_attributes": True
    }
