from pydantic import BaseModel
from typing import List, Optional, Dict

class Product(BaseModel):
    name: str
    name_ua: str
    article: str
    price: float
    commission_percent: int
    commission_sum: float
    sold: int
    price_old: float


class Purchases(BaseModel):
    id: int
    item_name: Optional[str] = None
    item: Product
    price: float
    quantity: int
    cost: float
    cost_with_discount: float
 

class UserTitle(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    second_name: Optional[str] = None
    full_name: str

class DeliveryCity(BaseModel):
    id: int
    uuid: str
    city_name: str
    name: str
    region_title: str
    title: str

class Delivery(BaseModel):
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
    city: DeliveryCity
    delivery_method_id: int
    ref_id: Optional[str] = None
    name_logo: str
    email: Optional[str] = None
    reserve_date: Optional[str] = None
    delivery_date: Optional[str] = None

class Payment(BaseModel):
    payment_method_id: int
    payment_method_name: str
    payment_type: str
    payment_type_title: str
    payment_status: dict|None
    credit: Optional[float] = None

class StatusPayment(BaseModel):
    order_id: int
    status_payment_id: int
    name: str
    title: str
    value: int
    payment_invoice_id: int
    created_at: str

class OrderRoz(BaseModel):
    amount: float
    amount_with_discount: float
    cost: float
    cost_with_discount: float
    payment: Payment

    id: int
    market_id: int
    created: str
    changed: str

    delivery: Delivery
    from_warehouse: bool
    ttn: str

    recipient_title: UserTitle
    recipient_phone: str

    comment: Optional[str] = None
    status: int
    status_group: int
    status_payment: StatusPayment|None
    seller_comment: List[str]

    user_phone: str
    user_title: UserTitle
    user_rating: int
    
    items_photos: List[dict]
    total_quantity: int
    purchases: List[Purchases]
