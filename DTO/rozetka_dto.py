from pydantic import BaseModel
from typing import List, Optional, Dict

class ProductRozetka(BaseModel):
    name: str
    name_ua: str
    article: str
    price: float
    commission_percent: int
    commission_sum: float
    sold: int
    price_old: float


class PurchasesRozetka(BaseModel):
    id: int
    item_name: Optional[str] = None
    item: ProductRozetka
    price: float
    quantity: int
    cost: float
    cost_with_discount: float
 

class UserTitleRozetka(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    second_name: Optional[str] = None
    full_name: str

class DeliveryCityRozetka(BaseModel):
    id: int
    uuid: str
    city_name: str
    name: str
    region_title: str
    title: str

class DeliveryRozetka(BaseModel):
    delivery_service_id: int
    delivery_service_name: str
    recipient_title: str
    recipient_first_name: str
    recipient_last_name: str
    recipient_phone: str
    another_recipient: bool
    place_id: int
    place_street: str
    place_number: str
    place_house: str
    city: DeliveryCityRozetka
    delivery_method_id: int
    ref_id: Optional[str] = None
    name_logo: str
    email: Optional[str] = None
    reserve_date: Optional[str] = None
    delivery_date: Optional[str] = None

class PaymentRozetka(BaseModel):
    payment_method_id: int
    payment_method_name: str
    payment_type: str
    payment_type_title: str
    payment_status: dict|None
    credit: Optional[float] = None

class StatusPaymentRozetka(BaseModel):
    order_id: int
    status_payment_id: int
    name: str
    title: str
    value: int
    payment_invoice_id: int
    created_at: str

class OrderRozetkaDTO(BaseModel):
    amount: float
    amount_with_discount: float
    cost: float
    cost_with_discount: float
    payment: PaymentRozetka

    id: int
    market_id: int
    created: str
    changed: str

    delivery: DeliveryRozetka
    from_warehouse: bool
    ttn: str

    recipient_title: UserTitleRozetka
    recipient_phone: str

    comment: Optional[str] = None
    status: int
    status_group: int
    status_payment: StatusPaymentRozetka|None
    seller_comment: List[str]

    user_phone: str
    user_title: UserTitleRozetka
    user_rating: int|None
    
    items_photos: List[dict]
    total_quantity: int
    purchases: List[PurchasesRozetka]
