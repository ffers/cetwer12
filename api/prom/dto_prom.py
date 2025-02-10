from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class CPACommission(BaseModel):
    amount: str
    is_refunded: Optional[bool] = False

class NameMultilang(BaseModel):
    ru: str
    uk: str

class Product(BaseModel):
    id: int
    external_id: str
    image: str
    quantity: int
    price: str
    url: str
    name: str
    name_multilang: NameMultilang
    total_price: str
    measure_unit: str
    sku: str
    cpa_commission: CPACommission

class DeliveryOption(BaseModel):
    id: int
    name: str
    shipping_service: Optional[str] = None

class DeliveryProviderData(BaseModel):
    provider: str
    type: str
    sender_warehouse_id: Optional[str] = None
    recipient_warehouse_id: str
    declaration_number: Optional[str] = None
    unified_status: Optional[str] = None

class PaymentOption(BaseModel):
    id: int
    name: str

class PaymentData(BaseModel):
    type: str
    status: str
    status_modified: str

class UTM(BaseModel):
    medium: str
    source: str
    campaign: str

class PSPromotion(BaseModel):
    name: str
    conditions: List[str]

class Cancellation(BaseModel):
    title: str
    initiator: str

class OrderDTO(BaseModel):
    id: int
    date_created: str
    client_first_name: str
    client_second_name: str
    client_last_name: str
    client_id: int
    client_notes: str
    products: List[Product]
    phone: str
    email: str
    price: str
    full_price: str
    delivery_option: DeliveryOption
    delivery_provider_data: DeliveryProviderData
    delivery_address: str
    delivery_cost: int
    payment_option: PaymentOption
    payment_data: PaymentData
    status: str
    status_name: str
    source: str
    price_with_special_offer: Optional[str] = None
    special_offer_discount: Optional[str] = None
    special_offer_promocode: Optional[str] = None
    has_order_promo_free_delivery: bool
    cpa_commission: CPACommission
    utm: UTM
    dont_call_customer_back: bool
    ps_promotion: Optional[PSPromotion] = None
    cancellation: Optional[Cancellation] = None
