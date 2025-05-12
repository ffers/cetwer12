from dataclasses import dataclass
from datetime import datetime

@dataclass
class CrmDTO:
    id: int = None
    name: str = ''
    timestamp: datetime = None
    user_id: int = None
