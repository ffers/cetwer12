# from typing import Optional, List
# from pydantic import BaseModel


# class ClientDTO(BaseModel):
#     first_name: str
#     last_name: str
#     second_name: Optional[str] = ""
#     id: int


# class DeliveryOptionDTO(BaseModel):
#     id: int
#     name: str
#     shipping_service: Optional[str]


# class DeliveryProviderDataDTO(BaseModel):
#     provider: str
#     type: str
#     sender_warehouse_id: Optional[str]
#     recipient_warehouse_id: Optional[str]
#     declaration_number: Optional[str]
#     unified_status: Optional[str]


# class PaymentOptionDTO(BaseModel):
#     id: int
#     name: str


# class NameMultilangDTO(BaseModel):
#     ru: str
#     uk: str


# class CPACommissionDTO(BaseModel):
#     amount: str
#     is_refunded: Optional[bool] = None


# class ProductDTO(BaseModel):
#     id: int
#     external_id: str
#     name: str
#     name_multilang: NameMultilangDTO
#     sku: str
#     price: str
#     quantity: float
#     measure_unit: str
#     image: str
#     url: str
#     total_price: str
#     cpa_commission: CPACommissionDTO


# class UTMDTO(BaseModel):
#     medium: str
#     source: str
#     campaign: str


# class PromOrderDTO(BaseModel):
#     id: int
#     date_created: str
#     date_modified: str
#     client_first_name: str
#     client_second_name: str
#     client_last_name: str
#     client_id: int
#     client: ClientDTO
#     delivery_recipient: dict
#     email: Optional[str]
#     phone: str
#     delivery_option: DeliveryOptionDTO
#     delivery_address: str
#     delivery_provider_data: DeliveryProviderDataDTO
#     delivery_cost: float
#     payment_option: PaymentOptionDTO
#     payment_data: Optional[str]
#     price: str
#     full_price: str
#     client_notes: str
#     products: List[ProductDTO]
#     status: str
#     status_name: str
#     source: str
#     price_with_special_offer: Optional[str]
#     special_offer_discount: Optional[str]
#     special_offer_promocode: Optional[str]
#     has_order_promo_free_delivery: bool
#     cpa_commission: CPACommissionDTO
#     utm: UTMDTO
#     dont_call_customer_back: bool
#     ps_promotion: Optional[str]
#     cancellation: Optional[str]
