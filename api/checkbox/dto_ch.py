
from typing import List, Optional
from pydantic import BaseModel

class GoodDiscount(BaseModel):
    type: str  # "DISCOUNT"/"EXTRA_CHARGE"
    mode: str  # "VALUE"/"PERCENT"
    value: int
    tax_code: Optional[int] = None
    tax_codes: Optional[List[int]] = None
    name: Optional[str] = None
    privilege: Optional[str] = None

class Good(BaseModel):
    code: str
    name: str
    price: int  # price in cents
    tax: List[str]
    barcode: Optional[str] = None
    excise_barcodes: Optional[List[str]] = None
    header: Optional[str] = None
    footer: Optional[str] = None
    uktzed: Optional[str] = None

class GoodItem(BaseModel):
    good: Good
    good_id: Optional[str] = None
    quantity: int  # quantity in thousands (1 unit = 1000)
    is_return: Optional[bool] = False
    is_winnings_payout: Optional[bool] = False
    discounts: Optional[List[GoodDiscount]] = None
    total_sum: Optional[int] = None

class Delivery(BaseModel):
    email: Optional[str] = None
    emails: Optional[List[str]] = None
    phone: Optional[str] = None

class ReceiptDiscount(BaseModel):
    type: str  # "DISCOUNT"/"EXTRA_CHARGE"
    mode: str  # "VALUE"/"PERCENT"
    value: int
    tax_code: Optional[int] = None
    tax_codes: Optional[List[int]] = None
    name: Optional[str] = None
    privilege: Optional[str] = None

class Bonus(BaseModel):
    bonus_card: Optional[str] = None
    value: Optional[int] = None
    additional_info: Optional[str] = None

class Payment(BaseModel):
    type: str  # "CASH"/"CASHLESS"
    pawnshop_is_return: Optional[bool] = None
    provider_type: Optional[str] = None
    code: Optional[int] = None
    value: int
    commission: Optional[int] = None
    label: Optional[str] = None
    card_mask: Optional[str] = None
    bank_name: Optional[str] = None
    auth_code: Optional[str] = None
    rrn: Optional[str] = None
    payment_system: Optional[str] = None
    owner_name: Optional[str] = None
    terminal: Optional[str] = None
    acquirer_and_seller: Optional[str] = None
    receipt_no: Optional[str] = None
    signature_required: Optional[bool] = None
    tapxphone_terminal: Optional[str] = None

class Custom(BaseModel):
    html_global_header: Optional[str] = None
    html_global_footer: Optional[str] = None
    html_body_style: Optional[str] = None
    html_receipt_style: Optional[str] = None
    html_ruler_style: Optional[str] = None
    html_light_block_style: Optional[str] = None
    text_global_header: Optional[str] = None
    text_global_footer: Optional[str] = None

class ReceiptDTO(BaseModel):
    id: str
    cashier_name: str
    departament: str
    goods: List[GoodItem]
    delivery: Optional[Delivery] = None
    discounts: Optional[List[ReceiptDiscount]] = None
    bonuses: Optional[List[Bonus]] = None
    payments: List[Payment]
    rounding: Optional[bool] = None
    header: Optional[str] = None
    footer: Optional[str] = None
    barcode: Optional[str] = None
    order_id: Optional[str] = None
    related_receipt_id: Optional[str] = None
    previous_receipt_id: Optional[str] = None
    technical_return: Optional[bool] = None
    is_pawnshop: Optional[bool] = None
    custom: Optional[Custom] = None

class Shift(BaseModel):
    
