

import os

from pydantic import BaseModel

from utils import OC_logger

from DTO.order_dto import \
    OrderDTO, ProductDto, \
    CostumerDto, RecipientDto

from DTO import \
    OrderRozetkaDTO


from a_service import ProductServ

class RozetkaMapper():
    def __init__(self, product_serv: ProductServ):
        self.product_serv = product_serv 
        self.logger = OC_logger.oc_log('rozetka_mapper')
 
    def order(self, data: OrderRozetkaDTO, store_id) -> OrderDTO:
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
            ttn_ref=None,  # Приклад для поля ttn_ref
            delivery_option=data.delivery.delivery_service_name,
            city_name=data.delivery.city.city_name,
            city_ref=data.delivery.city.uuid,
            region=data.delivery.city.region_title,
            area=data.delivery.city.region_title,
            warehouse_option=str(data.delivery.delivery_method_id),
            warehouse_text=warehouse_text,
            warehouse_ref=data.delivery.ref_id,
            sum_price=data.amount,
            sum_before_goods=None,
            description=data.comment,
            description_delivery=f"Замовлення Rozetka Vida {data.id}",
            cpa_commission=self.get_cpa(data.purchases),
            client_id=None,
            send_time=None,
            order_id_sources=None,
            order_code=f"R-{data.id}",
            payment_status_id=None,
            ordered_status_id=10,
            warehouse_method_id=self.warehouse_method(data.delivery.delivery_method_id),
            source_order_id=3,
            payment_method_id=self.payment_method(data.payment),
            delivery_method_id=self.delivery_method(data.delivery),
            author_id=55,
            ordered_product=self.product(data.purchases),
            recipient=self.recipient(data),
            recipient_id=None,
            costumer=self.costumer(data),
            costumer_id=None,
            store_id=store_id,
            client_firstname=data.user_title.first_name,
            client_lastname=data.user_title.last_name,
            client_surname=data.user_title.second_name,
            quantity_orders_costumer=None
        )


    
    def costumer(self, data):
        return CostumerDto(
        first_name=data.user_title.first_name,
        last_name=data.user_title.last_name,
        second_name=data.user_title.second_name,
        phone=data.recipient_phone,
        email=None
        )
    
    def recipient(self, data):
        return RecipientDto(
        first_name=data.recipient_title.first_name,
        last_name=data.recipient_title.last_name,
        second_name=data.recipient_title.second_name,
        phone=data.user_phone,
        email=None
        )
    
    def warehouse_method(self, d):
        mapping = {
            1: 1,
            2: 2,
        }
        return mapping.get(d)  

    def load_product(self, artcl, name):
        product = self.product_serv.load_item_by_article(artcl, name)
        return product.id      

    def get_cpa(self, data):
        result = 0
        for p in data:
            result += p.item.commission_sum
        return str(result)
            
    def product(self, data):
        result = []

        for item in data:
            print("product", item)
            artcl = item.item.article
            name = item.item.name_ua
            dto = ProductDto(
                id=None,
                quantity=item.quantity,
                price=item.price,
                order_id=None,
                product_id=self.load_product(artcl, name),
            )
            result.append(dto)

        return result

    
    def delivery_method(self, delivery):
        del_id = delivery.delivery_service_id
        avalaible = {
            5: 1,
            1: 2,
            2024: 3,
            14383961: 4,
            13013935: 5, 
            43660: 1,
            56214: 2,
        }
        return avalaible[del_id] if del_id in avalaible else self.new_delivery(delivery)

    
    
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
            6815: 6,
            4682: 2
        }
        return mapping[pay_id] if pay_id in mapping else self.new_payment(payment)

    
    def new_payment(self, payment):
        name=payment.payment_method_name
        ind=payment.payment_method_id
        self.logger.error(f'new_payment: name-{name}, id-{ind}')
        if os.getenv('ENV') != 'dev': return 7 
        else: return 8
         

       