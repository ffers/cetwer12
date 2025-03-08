from server_flask.models import Orders, OrderedProduct
from server_flask.db import db
from sqlalchemy import desc
from urllib.parse import unquote
from datetime import datetime, timedelta

 

class OrderRep:

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
                        description_delivery="Одяг Jemis",
                        order_code=item.order_code
                        )
            db.session.add(order)
            db.session.commit()
            return order
        except:
            return False
    
    def add_ordered_product(self, p):
        product_obj = OrderedProduct(
            quantity=p.quantity,
            price=p.price,
            order_id=p.order_id,
            product_id=p.product_id
        )
        db.session.add(product_obj)
        db.session.commit()
        return product_obj

    def update_history(self, order_id, new_comment):
        # try:
            order = self.load_item(order_id)
            if order.history:
                new_comment = order.history + new_comment
            order.history = new_comment
            db.session.commit()
            return True
        # except:
        #     return False


    def load_item(self, order_id):
        item = Orders.query.get_or_404(int(order_id))
        return item

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
            items = Orders.query.filter_by(**{search_param: search_value}).order_by(desc(Orders.timestamp)).all()
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

    def add_ttn_crm(self, id, ttn):
        try:
            order = self.load_item(id)
            order.ttn = ttn
            db.session.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    def update_time_send(self, id, send_time):
        try:
            item = self.load_item(id)
            item.send_time = send_time
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







