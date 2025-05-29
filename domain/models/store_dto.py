from dataclasses import dataclass

@dataclass
class StoreDTO:
    id: int = None
    name: str = ''
    api: str = ''
    token: str = ''
    token_market: str = ''
