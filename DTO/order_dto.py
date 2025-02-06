from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Product(BaseModel):
    quantity: int
    price: float
    order_id: int|None
    product_id: int|None
    article: str|None
    
    # class Config:
    #     allow_mutation = True


class OrderDTO(BaseModel):
    timestamp: datetime
    phone: str
    email: Optional[str] = None
    ttn: str|None
    ttn_ref: Optional[str]
    client_firstname: Optional[str] = None
    client_lastname: Optional[str] = None
    client_surname: Optional[str] = None
    delivery_option: str
    city_name: str
    city_ref: Optional[str]
    region: str
    area: Optional[str]
    warehouse_option: int|None
    warehouse_text: str|None
    warehouse_ref: str|None
    sum_price: float
    sum_before_goods: Optional[float] = None
    description: Optional[str]
    description_delivery: Optional[str]
    cpa_commission: Optional[str]
    client_id: int|None
    send_time: Optional[datetime]
    order_id_sources: Optional[str]
    order_code: str
    prompay_status_id: Optional[int] = None
    ordered_status_id: Optional[int]
    warehouse_method_id: Optional[int]
    source_order_id: Optional[int]
    payment_method_id: Optional[int]
    payment_method_name: str|None
    delivery_method_id: Optional[int]
    author_id: Optional[int] = None
    # comments: None
    # likes: List[LikesDTO] = []
    ordered_product: List[Product]
    # delvery_order: Optional[DeliveryOrderDTO] = None
    # prompay_status: Optional[PrompayStatusDTO] = None
    # ordered_status: Optional[OrderedStatusDTO] = None
    # warehouse_method: Optional[WarehouseMethodDTO] = None
    # source_order: Optional[SourceOrderDTO] = None
    # payment_method: Optional[PaymentMethodDTO] = None
    # delivery_method: Optional[DeliveryMethodDTO] = None

class Config:
    orm_mode = True


