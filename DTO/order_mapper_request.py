from flask import request
from datetime import datetime
from DTO import OrderDTO, ProductDto, CostumerDto, RecipientDto
from urllib.parse import unquote    

class OrderFormMapper:
    def from_request(self, req: request) -> OrderDTO:
        form = req.form

        costumer = CostumerDto(
            first_name=form.get('costumer_firstname'),
            last_name=form.get('costumer_lastname'),
            second_name=form.get('costumer_secondname'),
            phone=form.get('costumer_phone'),
            email=form.get('costumer_email'),
        )

        recipient = RecipientDto(
            first_name=form.get('recipient_firstname'),
            last_name=form.get('recipient_lastname'),
            second_name=form.get('recipient_secondname'),
            phone=form.get('recipient_phone'),
            email=None,
        )

        products = self._parse_products(form)
        sum_before_goods=self._sum_before_goods(form)

        order = OrderDTO(
            timestamp=datetime.now(),
            phone=form.get('costumer_phone'),
            email=form.get('costumer_email'),
            ttn=form.get('ttn'),
            ttn_ref=None,
            client_firstname=form.get('costumer_firstname'),
            client_lastname=form.get('costumer_lastname'),
            client_surname=form.get('costumer_middlename'),
            city_name=form.get('CityName'),
            city_ref=form.get('CityREF'),
            region='', 
            area=None,
            warehouse_option=form.get('warehouse_option'),  
            warehouse_text=unquote(form.get('warehouse-text')),
            warehouse_ref=form.get('warehouse-id'),
            sum_price=float(form.get('total-all', 0)),
            sum_before_goods=sum_before_goods,
            description=form.get('description'),
            description_delivery=form.get('description_delivery'),
            cpa_commission=None,
            client_id=None,
            send_time=None,
            delivery_option=None, # розглядай видалення
            order_id_sources=None,
            order_code=form.get('order_code', None),
            prompay_status_id=None, 
            ordered_status_id=form.get('order_status_id'),  
            warehouse_method_id=None,
            source_order_id=int(form.get('source_order_id')),
            delivery_method_id=form.get('delivery_method'),
            payment_method_id=form.get('payment_option'),
            author_id=form.get('author_id'),
            recipient=recipient,
            recipient_id=form.get('recipient_id', None),
            costumer=costumer,
            costumer_id=form.get('costumer_id', None),
            ordered_product=products
        )

        return order


    def update_order_dto_from_session(self, session_data, form):
        print("update_order_dto_from_session", form)
        order_data = session_data
        products = self._parse_products(form)
        sum_before_goods=self._sum_before_goods(form)

        order_data.update({
            "phone": form.get('costumer_phone'),
            "email": form.get('costumer_email'),
            "ttn": form.get('ttn'),
            "client_firstname": form.get('costumer_firstname'),
            "client_lastname": form.get('costumer_lastname'),
            "client_surname": form.get('costumer_middlename'),
            "city_name": form.get('CityName'),
            "city_ref": form.get('CityREF'),
            "warehouse_option": form.get('warehouse_option'),
            "warehouse_text": unquote(form.get('warehouse-text')),
            "warehouse_ref": form.get('warehouse-id'),
            "sum_price": float(form.get('total-all', 0)),
            "sum_before_goods": sum_before_goods,
            "description": form.get('description'),
            "delivery_method_id": form.get('delivery_method'),
            "payment_method_id": form.get('payment_option'),
            "ordered_product": products
        })

        return order_data



    def _parse_products(self, form):        
        quantities = form.getlist('quantity')
        prices = form.getlist('price')
        product_ids = form.getlist('product_id')
        zip_product = zip(quantities, prices, product_ids)
        resp = self.make_product(zip_product)
        return resp

    def make_product(self, zip_product):
        products = []
        for qty, price, pid in zip_product:
            product_dto = ProductDto(
                product_id=int(pid) if pid else None,
                quantity=int(qty),
                price=float(price),
                order_id=None
            )
            products.append(product_dto)
        return products

    def _sum_before_goods(self, form):
        sum = form.get('sum_before_goods', None)
        if sum:
            return sum
        else:
            return None