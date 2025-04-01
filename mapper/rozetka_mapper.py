from pydantic import BaseModel

from DTO.order_dto import \
    OrderDTO, ProductDto, \
    CostumerDto, RecipientDto

from DTO import \
    OrderRozetkaDTO


from a_service import ProductServ

class RozetkaMapper():
    def __init__(self, product_serv: ProductServ):
        self.product_serv = product_serv()  
 
    def order(self, data: OrderRozetkaDTO) -> OrderDTO:
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
            description_delivery=f"Замовлення Rozetka Jerni {data.id}",
            cpa_commission=None,
            client_id=None,
            send_time=None,
            order_id_sources=None,
            order_code=f"R-{data.id}",
            payment_status_id=None,
            ordered_status_id=10,
            warehouse_method_id=self.warehouse_method(data.delivery.delivery_method_id),
            source_order_id=3,
            payment_method_id=self.payment_method(data.payment.payment_method_id),
            payment_method_name=data.payment.payment_method_name,
            delivery_method_id=self.delivery_method(data.delivery.delivery_service_id),
            author_id=55,
            ordered_product=self.product(data.purchases),
            recipient=self.recipient(data),
            recipient_id=None,
            costumer=self.costumer(data),
            costumer_id=None,
            client_firstname=data.user_title.first_name,
            client_lastname=data.user_title.last_name,
            client_surname=data.user_title.second_name
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

    def load_product_by_article(self, artcl):
        product = self.product_serv.load_item_by_article(artcl)
        return product.id         
            
    def product(self, data):
        result = []

        for item in data:
            print("product", item)
            dto = ProductDto(
                id=None,
                quantity=item.quantity,
                price=item.price,
                order_id=None,
                product_id=self.load_product_by_article(item.item.article),
            )
            result.append(dto)

        return result

    
    def delivery_method(self, order):
        mapping = {
            5: 1,
            1: 2,
            2024: 3,
            14383961: 4,
            13013935: 5, 
            43660: 1
        }
        return mapping.get(order)
    
    def payment_method(self, order):
        mapping = {
            1: 1,
            6211: 2,
            11111111: 3,
            11111111: 4,
            11111111: 5,
            4524: 6,
        }
        return mapping.get(order)

       