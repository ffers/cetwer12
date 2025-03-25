from flask import request
from datetime import datetime
from DTO import OrderDTO, ProductDto, CostumerDto, RecipientDto
from urllib.parse import unquote    

class OrderFormMapper:
    @staticmethod
    def from_request(req: request) -> OrderDTO:
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

        products = OrderFormMapper._parse_products(req)

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
            sum_before_goods=None,
            description=form.get('description'),
            description_delivery=None,
            cpa_commission=None,
            client_id=None,
            send_time=None,
            delivery_option=None, # розглядай видалення
            order_id_sources=None,
            order_code=form.get('order_code'),
            prompay_status_id=None, 
            ordered_status_id=None,  
            warehouse_method_id=None,
            source_order_id=None,
            delivery_method_id=form.get('delivery_method'),
            payment_method_id=form.get('payment_option'),
            author_id=None,
            recipient=recipient,
            recipient_id=form.get('recipient_id'),
            costumer=costumer,
            costumer_id=form.get('costumer_id'),
            ordered_product=products
        )

        return order

    @staticmethod
    def _parse_products(req: request):
        products = []
        articles = req.form.getlist('old_product_art')
        quantities = req.form.getlist('quantity')
        prices = req.form.getlist('price')
        product_ids = req.form.getlist('product')

        for art, qty, price, pid in zip(articles, quantities, prices, product_ids):
            product_dto = ProductDto(
                article=art,
                product_id=int(pid) if pid else None,
                quantity=int(qty),
                price=float(price),
                order_id=None
            )
            products.append(product_dto)

        return products

    @staticmethod
    def _sum_before_goods(form):
        sum = form.get('sum_before_goods')
        if sum:
            return sum
        else:
            return None