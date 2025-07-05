import os
from server_flask.models import Orders
from pydantic import BaseModel
from utils import OC_logger
from DTO.order_dto import \
    OrderDTO, ProductDto, \
    CostumerDto, RecipientDto





def map_order_to_dto(order: Orders):
    return OrderDTO(
    id=order.id,
    order_code=order.order_code,
    timestamp=order.timestamp,
    phone=order.phone,
    email=order.email,
    ttn=order.ttn,
    ttn_ref=order.ttn_ref,
    client_firstname=order.client_firstname,
    client_lastname=order.client_lastname,
    client_surname=order.client_surname,
    description=order.description,
    history=order.history,
    delivery_option=order.delivery_option,
    city_name=order.city_name,
    city_ref=order.city_ref,
    region=order.region,
    area=order.area,
    warehouse_option=order.warehouse_option,
    warehouse_text=order.warehouse_text,
    warehouse_ref=order.warehouse_ref,
    sum_price=order.sum_price,
    sum_before_goods=order.sum_before_goods,
    description_delivery=order.description_delivery,
    cpa_commission=order.cpa_commission,
    client_id=order.client_id,
    send_time=order.send_time,
    order_id_sources=order.order_id_sources,
    payment_status_id=order.payment_status_id,
    ordered_status_id=order.ordered_status_id,
    warehouse_method_id=order.warehouse_method_id,
    source_order_id=order.source_order_id,
    payment_method_id=order.payment_method_id,
    delivery_method_id=order.delivery_method_id,
    author_id=order.author_id,
    recipient_id=order.recipient_id,
    recipient=RecipientDto.model_validate(order.recipient),
    costumer_id=order.costumer_id,
    costumer=CostumerDto.model_validate(order.costumer),
    store_id=order.store_id,
    quantity_orders_costumer=order.quantity_orders_costumer,
    ordered_product=[
        ProductDto.model_validate(p) for p in order.ordered_product
    ]
)