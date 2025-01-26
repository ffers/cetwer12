from pydantic import BaseModel
from typing import List, Optional


class GoodItem(BaseModel):
    code: str
    name: str
    price: str
    quantity: int 

class Payment(BaseModel):
    type: str  # "CASH"/"CASHLESS"
    code: str
    value: int

class ReceiptDTO(BaseModel):
    receipt_id: str
    shift_id: str
    cashier_name: str
    departament: str
    goods: List[GoodItem]
    payments: List[Payment]
    total_sum: int
    
class ShiftDTO(BaseModel):
    shifd_id: str
    open: str
    closed: str
