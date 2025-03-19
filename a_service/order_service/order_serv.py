import random
from flask import jsonify
from utils.my_time_util import my_time

from .client_serv import OrderProcessingPipeline

from repository import OrderRep
from .order_api_process import OrderApi
from ..telegram_handler.text_formater.text_order_manager import TextOrderManager  



class OrderServ:
    def __init__(self):
        self.order_rep = OrderRep()

    def generate_order_code(self, prefix='ASX'):
        digits = [random.choice('0123456789') for _ in range(6)]
        unique_id = ''.join(digits)  # Генеруємо унікальний ID та беремо перші 6 символів
        order_code = f'{prefix}-{unique_id}'
        return order_code

        #нужно написать функцію для копирования всех кліентов
        # в другую таблицу с записью установленого айди в главной таблице
    def update_client_info(self):
        orders = self.order_rep.load_item_all()
        resp = self.change_order(orders)
        if not resp:
            print("change_order: Невийшло")
        return True

    def change_order(self, orders):
        for order in orders:
            resp = self.create_client(order)
            if not resp:
                break
        return resp
  
            # нужно создать костюмера
            # нужно создать отримувача

    def create_client(self, order):
        resp = "without answer"
        # try: 
        resp = OrderProcessingPipeline().process(order)
        if not resp:
            raise
        return resp
        # except:
        #     print("create_client:", resp)
        #     return False


    def load_orders_store(self, api_name, OrderCntrl, TelegramCntrl, EvoClient, RozetMain):
        order_api = OrderApi(api_name, OrderCntrl, TelegramCntrl, EvoClient, RozetMain)
        telegram_cntrl = TelegramCntrl()
        return order_api.get_orders()

        # if orders:
        #     return self.observer_order(orders, telegram_cntrl)
        # else: 
        #     return False

    def observer_order(self, orders, telegram_cntrl):
        for order in orders:
            order_db = self.add_order2(order)
            if order_db:
                text_order = TextOrderManager(order_db).builder()
                telegram_cntrl.sendMessage(telegram_cntrl.chat_id_confirm, text_order)
        return True 

    def add_order2(self, order_dto):
        order_db = self.order_rep.add_order(order_dto)
        if order_db:
            for product in order_dto.ordered_product:
                product_db = self.add_ordered_product(product, order_db.id)
        order_db = self.order_rep.load_item(order_db.id)
        return order_db

    def add_ordered_product(self, product_dto, ord_id, ProductCntrl):
        prod_cntrl = ProductCntrl()
        prod_db = prod_cntrl.load_by_article(product_dto.article)
        product_dto.order_id = ord_id
        product_dto.product_id = prod_db.id
        product_db = self.ord_rep.add_ordered_product(product_dto)
        return product_db

    def update_history(self, order_id, comment):
        current_time = next(my_time()).strftime("%d-%m-%Y %H:%M")
        new_comment =  "\n" + f"{current_time}: " + comment
        return self.order_rep.update_history(order_id, new_comment)
    
    def change_history(self, request_data):
        form = request_data.form
        order_id = form.get("order_id")
        new_history = form.get("history") + "\n"
        current_time = next(my_time()).strftime("%d-%m-%Y %H:%M")
        new_history += f"{current_time}: Історія змінена"
        resp = self.order_rep.change_history(order_id, new_history)
        print("dev_change_history:", resp)
        return resp
    
 
    def search_for_order(self, order):
        order_list = []
        if order:
            for item in order:
                if item.order_code:
                    item_data = self.create_text(item)
                    order_list.append(item_data)
                    print(order_list)
            return jsonify({'results': order_list})
        return jsonify({'results': []})

    def create_text(self, item):
        product_text = ' '
        for product in item.ordered_product:
            product_text += product.products.article + ' '
        text = (item.order_code + ' '
                + item.client_lastname + ' '
                + item.client_firstname + ' '
                + product_text + ' ')
        item_data = {
            'id': item.id,
            'text': text
        }
        return item_data

    def replace_phone(self, phone):
        return phone

    def parse_dict_status(self, data):
        orders = data["id"]
        status = data["status"]
        return orders, status
    
