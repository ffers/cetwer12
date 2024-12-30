from pydantic import BaseModel
from typing import List, Optional

class CpaCommissionDTO(BaseModel):
    amount: str
    is_refunded: Optional[bool] = False

class ProductDTO(BaseModel):
    id: int
    external_id: Optional[str] = ""
    name: str
    name_multilang: dict
    sku: str
    price: str
    quantity: float
    measure_unit: str
    image: str
    url: str
    total_price: str
    cpa_commission: CpaCommissionDTO

class DeliveryOptionDTO(BaseModel):
    id: int
    name: str
    shipping_service: Optional[str] = None

class DeliveryProviderDataDTO(BaseModel):
    provider: str
    type: str
    sender_warehouse_id: Optional[str] = None
    recipient_warehouse_id: str
    declaration_number: Optional[str] = None
    unified_status: Optional[str] = None

class PaymentOptionDTO(BaseModel):
    id: int
    name: str

class UtmDTO(BaseModel):
    medium: str
    source: str
    campaign: str

class ClientDTO(BaseModel):
    first_name: str
    last_name: str
    second_name: Optional[str] = ""
    id: int

class OrderDTO(BaseModel):
    id: int
    date_created: str
    date_modified: str
    client_first_name: str
    client_second_name: str
    client_last_name: str
    client_id: int
    client: ClientDTO
    delivery_recipient: dict
    email: Optional[str] = None
    phone: str
    delivery_option: DeliveryOptionDTO
    delivery_address: str
    delivery_provider_data: DeliveryProviderDataDTO
    delivery_cost: float
    payment_option: PaymentOptionDTO
    payment_data: Optional[dict] = None
    price: str
    full_price: str
    client_notes: str
    products: List[ProductDTO]
    status: str
    status_name: str
    source: str
    price_with_special_offer: Optional[str] = None
    special_offer_discount: Optional[str] = None
    special_offer_promocode: Optional[str] = None
    has_order_promo_free_delivery: bool
    cpa_commission: CpaCommissionDTO
    utm: UtmDTO
    dont_call_customer_back: bool
    ps_promotion: Optional[str] = None
    cancellation: Optional[str] = None
