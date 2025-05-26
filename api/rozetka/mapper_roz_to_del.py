from pydantic import BaseModel
from DTO.order_dto import OrderDTO, ProductDto, CostumerDto, RecipientDto
from .dto_roz import OrderRoz
from utils import OC_logger

class MapperRozTOdEl():
    def __init__(self):
        self.logger = OC_logger.oc_log('api.mapper_roz')   
 
    def order(self, data: OrderRoz) -> OrderDTO:
        warehouse_text=(
            # f"{data.delivery.city.title} -" 
            f"{data.delivery.place_number} "
            f"{data.delivery.place_street} "
            f"{data.delivery.place_house}"
        )
        return OrderDTO(
            timestamp=data.created,  # чи інша дата з маркетплейсу
            phone=data.user_phone,
            email=data.delivery.email,
            ttn=None,
            ttn_ref=None,  # Приклад для поля ttn_re
            delivery_option=data.delivery.delivery_service_name,
            city_name=data.delivery.city.city_name,
            city_ref=data.delivery.city.uuid,
            region=data.delivery.city.region_title,
            area=data.delivery.city.region_title,
            warehouse_option=data.delivery.delivery_method_id,
            warehouse_text=warehouse_text,
            warehouse_ref=data.delivery.ref_id,
            sum_price=data.amount,
            sum_before_goods=None,
            description=data.comment,
            description_delivery=f"Замовлення Rozetka Jerni {data.id}",
            cpa_commission=None,
            client_id=None,
            send_time=None,
            order_id_sources=None,
            order_code=f"R-{data.id}",
            payment_status_id=None,
            ordered_status_id=10,
            warehouse_method_id=self.warehouse_method(data.delivery.delivery_service_id),
            source_order_id=3,
            payment_method_id=self.payment_method(data.payment.payment_method_id),
            delivery_method_id=self.delivery_method(data.delivery.delivery_service_id),
            author_id=55,
            ordered_product=self.product(data.purchases),
            recipient=self.recipient(data),
            costumer=self.costumer(data),
            client_firstname=data.user_title.first_name,
            client_lastname=data.user_title.last_name,
            client_surname=data.user_title.second_name
        )


    
    def costumer(self, data):
        return CostumerDto(
        first_name=data.user_title.first_name,
        last_name=data.user_title.last_name,
        second_name=data.user_title.second_name,
        phone=data.user_phone,
        )
    
    def recipient(self, data):
        return RecipientDto(
        first_name=data.recipient_title.first_name,
        last_name=data.recipient_title.last_name,
        second_name=data.recipient_title.second_name,
        phone=data.recipient_phone
        )
    
    def warehouse_method(self, d):
        mapping = {
            1: 1,
            2: 2,
        }
        return mapping.get(d)             
            
    def product(self, data):  
        return [ProductDto
                (
                quantity=product.quantity, 
                price=product.price,
                article=product.item.article,
                order_id=None,
                product_id=None,
                ) for product in data]
    
    
    def delivery_method(self, delivery):
        del_id = delivery.delivery_service_id
        avalaible = {
            5: 1,
            1: 2,
            2024: 3,
            14383961: 4,
            13013935: 5, 
            43660: 1
        }
        return avalaible.get(del_id, self.new_delivery(delivery))
    
    def new_delivery(self, delivery):       
        name=delivery.delivery_service_name
        ind=delivery.delivery_service_id
        self.logger.error(f'new_delivery: name-{name}, id-{ind}')
        return 6

    def payment_method(self, payment):
        pay_id = payment.payment_method_id
        mapping = {
            1: 1,
            6211: 2,
            11111111: 3,
            11111111: 4,
            11111111: 5,
            4524: 6,
        }
        return mapping.get(pay_id, self.new_payment(payment))
    
    def new_payment(self, payment):
        name=payment.payment_method_name
        ind=payment.payment_method_id
        self.logger.error(f'new_payment: name-{name}, id-{ind}')
        return 7


       