from server_flask.models import Orders, OrderedProduct, Costumer, Recipient
from server_flask.db import db
from sqlalchemy import desc
from urllib.parse import unquote
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from .exception_serv import OrderAlreadyExistsError

from utils import OC_logger

class OrderRep:
    def __init__(self):
        self.logger = OC_logger.oc_log('order_rep')

    def my_time(self):
        yield (datetime.utcnow())

    def add_order(self, item):
        try:
            order = Orders(description=item.description,
                        city_name=item.city_name,
                        city_ref=item.city_ref,
                        warehouse_text=item.warehouse_text,
                        warehouse_ref=item.warehouse_ref, 
                        phone=item.phone,
                        author_id=item.author_id,
                        client_firstname=item.client_firstname,
                        client_lastname=item.client_lastname,
                        client_surname=item.client_surname,
                        warehouse_option=item.warehouse_option,
                        delivery_option=item.delivery_option,
                        payment_method_id=item.payment_method_id,
                        sum_price=item.sum_price,
                        sum_before_goods=item.sum_before_goods,
                        delivery_method_id=item.delivery_method_id,
                        source_order_id=item.source_order_id,
                        ordered_status_id=item.ordered_status_id,
                        description_delivery=item.description_delivery,
                        order_code=item.order_code,
                        costumer_id=item.costumer_id,
                        recipient_id=item.recipient_id,
                        payment_status_id=item.payment_status_id
                        )
            db.session.add(order)
            db.session.commit()
            return order
        except IntegrityError as e:
            db.session.rollback()
            if "duplicate key" in str(e.orig):
                raise OrderAlreadyExistsError("Order already exists")
            print("add_order:", e)
        except Exception as e:
            return str(e)
    
    def update_order(self, order_id, order_dto):
        order = self.load_item(order_id)
        order.timestamp = order_dto.timestamp
        order.phone = order_dto.phone
        order.email = order_dto.email
        order.ttn = order_dto.ttn
        order.ttn_ref = order_dto.ttn_ref
        order.client_firstname = order_dto.client_firstname
        order.client_lastname = order_dto.client_lastname
        order.client_surname = order_dto.client_surname
        order.delivery_option = order_dto.delivery_option
        order.city_name = order_dto.city_name
        order.city_ref = order_dto.city_ref
        order.region = order_dto.region
        order.area = order_dto.area
        order.warehouse_option = order_dto.warehouse_option
        order.warehouse_text = order_dto.warehouse_text
        order.warehouse_ref = order_dto.warehouse_ref
        order.sum_price = order_dto.sum_price
        order.sum_before_goods = order_dto.sum_before_goods
        order.description = order_dto.description
        order.description_delivery = order_dto.description_delivery
        order.cpa_commission = order_dto.cpa_commission
        order.client_id = order_dto.client_id
        order.send_time = order_dto.send_time
        order.order_id_sources = order_dto.order_id_sources
        order.order_code = order_dto.order_code
        order.payment_status_id = order_dto.payment_status_id
        order.ordered_status_id = order_dto.ordered_status_id
        order.warehouse_method_id = order_dto.warehouse_method_id
        order.source_order_id = order_dto.source_order_id
        order.payment_method_id = order_dto.payment_method_id
        order.delivery_method_id = order_dto.delivery_method_id
        order.author_id = order_dto.author_id
        order.recipient_id = order_dto.recipient_id
        order.costumer_id = order_dto.costumer_id
        db.session.commit()
        db.session.refresh(order)
        return order
    
    def update_payment_status(self, order_id, status_id):
        order = self.load_item(order_id)
        try:
            order.payment_status_id = status_id
            db.session.commit()
            self.logger.info(f'Status payment change succes - id: {order_id}, status: {status_id}')
            return True
        except Exception as e:
            db.session.rollback()
            self.logger.error(f'Error: {e}')
            raise ValueError('Помилка при оновленні статусу оплати в реп')
        

    def update_ordered_product(self, order_id, products_dto):
        try:
            order = self.load_item(order_id)
            order.ordered_product.clear()

            for p in products_dto:
                ordered_product = OrderedProduct(
                    quantity=p.quantity,
                    price=p.price,
                    order_id=order_id,
                    product_id=p.product_id
                )
                order.ordered_product.append(ordered_product)

            db.session.commit()
            db.session.refresh(order)
            return  order
        except Exception as e:
            db.session.rollback()
            print("update_ordered_product error:", e)
            return False
    
    def load_ordered_product(self, item_id):
        return OrderedProduct.query.get_or_404(int(item_id)) 
    

    def update_history(self, order_id, new_comment):
        try:
            order = self.load_item(order_id)
            if order.history:
                new_comment = order.history + new_comment
            order.history = new_comment
            db.session.commit()
            return True
        except:
            return False
        
    def change_history(self, order_id, new_comment):
        try:
            order = self.load_item(order_id)
            print("devOrder_rep", new_comment)
            order.history = new_comment
            db.session.commit()
            return True
        except:
            return False

    def update_time_send(self, id, send_time):
        try:
            item = self.load_item(id)
            item.send_time = send_time
            db.session.commit()
            return True, None
        except Exception as e:
            return False, str(e)
        
    def update_model_from_dto(self, order_id, dto):
        model = self.load_item(order_id)
        for field, value in dto.model_dump().items():
            if value is not None and hasattr(model, field):
                setattr(model, field, value)
        db.session.commit()
        db.session.refresh(model)
        return model

        
    def update_new_dataclass(self, order_id: int, data):
        # Отримуємо поточний запис
        order = self.load_item(order_id)
        if not order:
            return None  # Якщо ордер не знайдено

        # Оновлюємо тільки ті атрибути, які не є `None`
        for key in data.__dataclass_fields__:  # Перебираємо поля `dataclass`
            value = getattr(data, key)
            if value is not None:
                setattr(order, key, value)

        # Зберігаємо зміни
        db.session.commit()
        db.session.refresh(order)
        return order  # Повертаємо оновлений об'єкт


    def load_item(self, order_id):
        try:
            item = Orders.query.get_or_404(int(order_id))
            return item
        except Exception as e:
            self.logger.error(f'Невдалося завантажити ордер id: {order_id}')
            raise ValueError('Нема такого замовлення')

    def load_item_all(self):
        item = Orders.query.all()
        return item

    def load_period_all(self):
        return Orders.query.filter_by(ordered_status_id=8).all()

    def load_status_id(self, id):
        return Orders.query.filter_by(ordered_status_id=id).order_by(desc(Orders.id)).all()

    def load_period(self, start, stop):
        items = Orders.query.filter(
            Orders.send_time >= start,
            Orders.send_time <= stop,
            Orders.ordered_status_id == 8
        ).all()
        return items

    def load_item_days(self):
        current_time = next(self.my_time())
        start_time = current_time - timedelta(hours=14)
        start_time = start_time.replace(hour=14, minute=0, second=0,
                                        microsecond=0)
        stop_time = start_time + timedelta(days=1)
        print(start_time)
        print(stop_time)
        items = Orders.query.filter(
            Orders.send_time >= start_time,
            Orders.send_time <= stop_time,
            Orders.ordered_status_id == 8
            ).all()

        return items

    def load_item_month(self):
        current_time = next(self.my_time())
        start_time = current_time - timedelta(hours=14)
        start_time = start_time.replace(day=1, hour=14, minute=0, second=0,
                                        microsecond=0)
        next_month = start_time.replace(day=28) + timedelta(days=4)
        stop_time = next_month - timedelta(days=next_month.day)

        print(start_time)
        print(stop_time)
        items = Orders.query.filter(
            Orders.send_time >= start_time,
            Orders.send_time <= stop_time,
            Orders.ordered_status_id == 8
            ).all()

        return items

    def load_all_for_searh_data(self, search_param, search_value):
        if search_value is not None:
            items = Orders.query.filter_by(
                **{search_param: search_value}
                ).order_by(
                    desc(Orders.timestamp)
                    ).all()
        else:
            items = Orders.query.order_by(desc(Orders.timestamp)).all()
        return items

    def load_for_np(self):
        item = Orders.query.filter(
            Orders.ordered_status_id == 2,
            Orders.delivery_method_id == 1
                                   ).all()
        return item

    def load_registred(self):
        item = Orders.query.filter(
            Orders.ordered_status_id == 11,
            Orders.delivery_method_id == 1
                                   ).all()
        return item

    def load_registred_roz(self):
        item = Orders.query.filter(
            Orders.ordered_status_id == 11,
            Orders.delivery_method_id == 2
                                   ).all()
        return item
    
    def load_unpaid_prom_orders(self):
            items = Orders.query.filter(
                Orders.ordered_status_id.in_([1, 10]),
                Orders.payment_method_id == 5,
                Orders.payment_status_id == 2
            ).all()
            return items


    def add_ttn_crm(self, id, ttn):
        try:
            order = self.load_item(id)
            order.ttn = ttn
            db.session.commit()
            return True, None
        except Exception as e:
            return False, str(e)




    def dublicate_item(self, item):
        order = Orders(description=item.description,
                       city_name=item.city_name,
                       city_ref=item.city_ref,
                       warehouse_text=item.warehouse_text,
                       warehouse_ref=item.warehouse_ref,
                       phone=item.phone,
                       author_id=item.author_id,
                       client_firstname=item.client_firstname,
                       client_lastname=item.client_lastname,
                       client_surname=item.client_surname,
                       warehouse_option=item.warehouse_option,
                       delivery_option=item.delivery_option,
                       payment_method_id=item.payment_method_id,
                       sum_price=item.sum_price,
                       sum_before_goods=item.sum_before_goods,
                       delivery_method_id=item.delivery_method_id,
                       source_order_id=1,
                       ordered_status_id=10,
                       description_delivery="Одяг Jemis")
        db.session.add(order)
        db.session.commit()
        return order

    def load_prod_order(self, id):
        item_all = OrderedProduct.query.filter_by(order_id=id).all()
        return item_all

    def load_for_order_code(self, id):
        item = Orders.query.filter_by(order_code=id).first()
        return item

    def load_for_code(self, id):
        item = Orders.query.filter_by(order_id_sources=str(id)).order_by(desc(Orders.timestamp)).first()
        return item

    def dublicate_order_prod(self, order_new, ord_prod_old):
        print(f"dublicate_order_prod {ord_prod_old}")
        for item in ord_prod_old:
            print(f"for_dublicate_order_prod {vars(item)}")
            ordered_product = OrderedProduct(product_id=item.product_id, price=item.price, quantity=item.quantity, order_id=order_new.id)
            order_new.ordered_product.append(ordered_product)
        db.session.commit()
        return True

    def change_status(self, order_id, status):
        order = self.load_item(order_id)
        order.ordered_status_id = status
        db.session.commit()
        return {"resp": True, "order_code": order.order_code, "ordered_status": order.ordered_status.name}

    def change_status_list(self, orders, status):
        for item in orders:
            order = self.load_item(item)
            order.ordered_status_id = status
            db.session.commit()
        return True

    def change_address(self, order_id, data):
        order = self.load_for_code(order_id)
        order.city_name = data["CityName"]
        order.city_ref = data["CityRef"]
        order.warehouse_text = data["WarehouseText"]
        order.warehouse_ref = data["WarehouseRef"]
        order.warehouse_method_id = data["WarehouseMethod"]
        db.session.commit()
        return True

    def add_order_code(self, order, code):
        order.order_id_sources = code
        order.order_code = code
        db.session.commit()
        return True

    def search_for_phone(self, phone):
        order = Orders.query.filter_by(phone=phone).all()
        return order

    def search_for_all(self, data):
        order = Orders.query.filter(
            (Orders.phone.ilike(f'%{data}%')) |
            (Orders.client_lastname.ilike(f'%{data}%')) |
            (Orders.client_surname.ilike(f'%{data}%')) |
            (Orders.client_firstname.ilike(f'%{data}%')) |
            (Orders.order_code.ilike(f'%{data}%')) |
            (Orders.ttn.ilike(f'%{data}%'))
        ).order_by(desc(Orders.id)).all()  
        return order

    def delete_order(self, id):
        task_to_delete = Orders.query.get_or_404(id)
        if task_to_delete:
            print(">>> Start delete in datebase")
            db.session.delete(task_to_delete)
            db.session.commit()
            print(">>> Delete in datebase")
            return True
        print(">>> Dont delete in datebase")
        return False


ord_rep = OrderRep()







