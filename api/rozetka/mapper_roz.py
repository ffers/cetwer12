from pydantic import BaseModel
from DTO import OrderDTO, Product
from .dto_roz import OrderRoz

class ClassName(BaseModel):
    def __init__(self):
        pass

    def map_marketplace_data_to_order_dto(self, data: OrderRoz) -> OrderDTO:
        # Маппінг об'єктів до OrderDTO
        return OrderDTO(
            timestamp=data.created,  # чи інша дата з маркетплейсу
            phone=data.user_phone,
            ttn=None,
            ttn_ref=None,  # Приклад для поля ttn_ref
            client_firstname=data.user_title.first_name,
            client_lastname=data.user_title.last_name,
            client_surname=data.user_title.second_name,
            delivery_option=data.delivery.delivery_service_name,
            city_name=data.delivery.city.city_name,
            city_ref=data.delivery.city.uuid,
            region=data.delivery.city.region_title,
            area=data.delivery.city.region_title,
            warehouse_option=data.warehouse_option,
            warehouse_text=data.warehouse_text,
            warehouse_ref=data.warehouse_ref,
            payment_option=data.payment.payment_method_name,
            sum_price=data.amount,
            sum_before_goods=None,
            description=data.comment,
            description_delivery=None,
            cpa_commission=None,
            client_id=None,
            send_time=None,
            order_id_sources=None,
            order_code=f"R-{data.id}",
            prompay_status_id=None,
            ordered_status_id=data.ordered_status_id,
            warehouse_method_id=data.delivery.delivery_method_id,
            source_order_id=3,
            payment_method_id=data.payment_method_id,
            delivery_method_id=data.delivery.delivery_service_id,
            author_id=None,
            ordered_product=self.product)
            
            
    def product(self, data):  
        return [Product
                (
                quantity=product.quantity, 
                price=product.price,
                order_id=None,
                product_id=
                ) for product in data.ordered_product],  # Перетворення продуктів
       