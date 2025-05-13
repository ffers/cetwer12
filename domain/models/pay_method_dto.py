from dataclasses import dataclass

@dataclass
class PayMethodDTO:
    id: int = None
    name: str = ''
    description: str = '' 

