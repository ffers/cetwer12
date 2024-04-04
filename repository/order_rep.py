from server_flask.models import Orders, OrderedProduct
from server_flask.db import db
from sqlalchemy import desc
from urllib.parse import unquote

class OrderRep:
    def load_item(self, order_id):
        item = Orders.query.get_or_404(order_id)
        return item

    def load_item_all(self):
        item = Orders.query.all()
        return item

    # def add_order(self, request):
    #     order = Orders(description=request.form['description'], city_name=request.form['CityName'],
    #                    city_ref=request.form['CityREF'],
    #                    warehouse_text=unquote(request.form['warehouse-text']),
    #                    warehouse_ref=request.form['warehouse-id'],
    #                    phone=request.form['phone'], author_id=current_user.id,
    #                    client_firstname=request.form['client_firstname'],
    #                    client_lastname=request.form['client_lastname'], client_surname=request.form['client_surname'],
    #                    warehouse_option=request.form['warehouse_option'], delivery_option="nova_poshta",
    #                    payment_method_id=request.form['payment_option'], sum_price=format_float(sum_price_draft),
    #                    sum_before_goods=sum_before_goods, delivery_method_id=1, source_order_id=1, ordered_status_id=10,
    #                    description_delivery="Одяг Jemis")
    #     db.session.add(order)
    #     db.session.commit()

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
        return order

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
        db.session.commit()
        return True

    def search_for_phon(self, phone):
        order = Orders.query.filter_by(phone=phone).all()
        return order

    def search_for_all(self, phone):
        order = Orders.query.filter(
    (Orders.phone.like(phone)) |
    (Orders.client_lastname.like(phone)) |
    (Orders.category.like(phone))
).all()
        return order










