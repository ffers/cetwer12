import random
from flask import jsonify
from utils import wrapper
from utils.my_time_util import my_time

from DTO import OrderDTO
from exceptions import OrderAlreadyExistsError
from repository import OrderRep, RecipientRep, CostumerRep

from .client_serv import OrderProcessingPipeline
from .status_new_with_payment import StatusNewWithPaidPipline
from .order_map_store_factory import OrderMapStoreFactory 
from .order_api_process import OrderApi

from ..telegram_handler.text_formater.text_order_manager import TextOrderManager  
from ..product_serv import ProductServ
from ..telegram_service import TgServNew
 
from copy import deepcopy


#  id |        name        | description
# ----+--------------------+-------------
#   1 | Підтвердити        |
#   2 | Підтвержено        |
#   3 | Оплачено           |
#   4 | Несплачено         |
#   5 | Скасовано          |
#   6 | Предзамовлення     |
#   7 | Питання            |
#   8 | Відправлено        |
#   9 | Отримано           |
#  10 | Нове               |
#  11 | Очікує відправленя |
#  12 | Виконано           |
#  13 | Тест
#  14 | Повернення
#  15 | Дубль              |

class OrderServ:
    def __init__(self):
        self.order_rep = OrderRep()
        self.costum_rep = CostumerRep()
        self.recip_rep = RecipientRep()
        self.prod_serv = ProductServ()
        self.map_ord = OrderMapStoreFactory
        self.tg = TgServNew()

    def generate_order_code(self, prefix='ASX'):
        digits = [random.choice('0123456789') for _ in range(6)]
        unique_id = ''.join(digits)  # Генеруємо унікальний ID та беремо перші 6 символів
        order_code = f'{prefix}-{unique_id}'
        if self.order_rep.load_for_code(order_code):
            self.generate_order_code()
        return order_code

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



    def observer_order(self, orders, telegram_cntrl):
        for order in orders:
            order_db = self.add_order2(order)
            if order_db:
                text_order = TextOrderManager(order_db).builder()
                keyboard_json = telegram_cntrl.keyboard_func()
                telegram_cntrl.sendMessage(
                                            telegram_cntrl.chat_id_confirm, 
                                            text_order,
                                            keyboard_json
                                           )
        return True 
    
    @wrapper()
    def add_costumer(self, costumer_dto):
        return self.costum_rep.create(costumer_dto)
    
    @wrapper()
    def add_recipient(self, recipient):
        return self.recip_rep.create(recipient)

    @wrapper()
    def add_order2(self, order_dto):
        order_db = self.order_rep.add_order(order_dto)
        if order_db:
            for product in order_dto.ordered_product:
                product_db = self.add_ordered_product(product, order_db.id)
        order_db = self.order_rep.load_item(order_db.id)
        return order_db
    

    def make_send_to_confirmed_tg_times(self, order):
        text_order = TextOrderManager(order).builder()
        keyboard_json = self.tg.keyboard_func()
        self.tg.sendMessage(self.tg.chat_id_confirm, 
                                text_order, keyboard_json)
        return True
    
    @wrapper()
    def add_order3(self, dto: OrderDTO):
        dto = self.check_order_code(dto)
        resp = self.add_costumer(dto)
        # print("add_order_costumer:", resp)
        resp = self.add_recipient(resp.get("result"))
        # print("add_order_recipient:", resp)
        dto = resp.get("result")
        resp = self.add_order4(resp.get("result"))
        # print("add_order_add_order:", resp)
        if resp:
            order = resp.get("result")
            products = dto.ordered_product
            order = self.order_rep.update_ordered_product(order.id, products)
            resp = True if order else False
            self.make_send_to_confirmed_tg_times(order)
            return order

        return resp 
    
    @wrapper()
    def add_order4(self, order_dto):
        return self.order_rep.add_order(order_dto)


    @wrapper()
    def add_costumer(self, dto):
        costumer = self.costum_rep.create(dto.costumer)
        dto.costumer_id = costumer.id
        return dto
    
    @wrapper()
    def add_recipient(self, dto):
        recipient = self.recip_rep.create(dto.recipient)
        dto.recipient_id = recipient.id
        return dto
    
    @wrapper()
    def add_ordered_product(self, product_dto, ord_id, ProductCntrl):
        prod_cntrl = ProductCntrl()
        prod_db = prod_cntrl.load_by_article(product_dto.article)
        product_dto.order_id = ord_id
        product_dto.product_id = prod_db.id
        product_db = self.ord_rep.add_ordered_product(product_dto)
        return product_db
    

    
    def load_orders_store(self, api_name, token, OrderCntrl, TelegramCntrl, EvoClient, RozetMain):
        resp = {}
        store = OrderApi(api_name, token, OrderCntrl, TelegramCntrl, EvoClient, RozetMain)
        list_order = store.get_orders()
        print("load_orders_store:", list_order)
        if list_order:
            for order in list_order:
                mapper = self.map_ord.factory(api_name, order)
                dto = mapper.process()
                resp.update(self.add_order3(dto))
                resp.update(store.change_status(dto.order_code, 1))
            return resp 
        else:
            return {"success": "ok", "order": "Store empty"}

    def load_status_id(self, id):
        if id == 10:
            result = StatusNewWithPaidPipline().process(self.order_rep)
           
            return result
        return self.order_rep.load_status_id(id)
      
    def check_order_code(self, order_dto):
        print("check_order_code:", order_dto.order_code)
        if not order_dto.order_code:
            order_dto.order_code = self.generate_order_code("ASX")
        return order_dto
    
    def update_order_front(self):
        pass

    @wrapper()
    def update_order3(self, order_id, order_dto):
        resp = {}
        print("update_order3:", order_dto)
        resp.update(self.update_costumer(order_dto))
        print("update_order3:", resp)
        resp.update(self.update_recipient(order_dto))
        print("update_order3:", resp)
        order_db = self.order_rep.update_order(order_id, order_dto)
        resp.update({"order_db": "ok"})
        if order_db:
            if order_dto.ordered_product:
                self.update_product3(order_dto, resp)
                self.make_send_to_confirmed_tg_times(order_db)
            return resp.update({"order_db": "ok"})
        resp.update({"order_db": "unsuccess"})
        return resp

    @wrapper()
    def update_product3(self, order_dto: OrderDTO, resp):
        products = order_dto.ordered_product
        product_db = self.order_rep.update_ordered_product(order_dto.id, products)
        return resp.update({"prod.id": "ok"}) if product_db else resp.update({"prod.article": "unsucces"})

    @wrapper()
    def update_costumer(self, dto):
        resp = self.costum_rep.update(dto.costumer_id, dto.costumer)
        if not resp:
            return {"costumer_update": "unsuccess"}
        return {"costumer_update": "ok"}
    
    @wrapper()
    def update_recipient(self, dto):
        resp = self.recip_rep.update(dto.recipient_id, dto.recipient)
        if not resp:
            return {"recipient_update": "unsuccess"}
        return {"recipient_update": "ok"}
    
    def update_client_info(self):
        orders = self.order_rep.load_item_all()
        resp = self.change_order(orders)
        if not resp:
            print("change_order: Невийшло")
        return True
    
    def update_ordered_product(self, order_id, products):
        print("update_ordered_product:", products)
        order = self.order_rep.update_ordered_product(order_id, products)
        resp = True if order else False
        return order
    

    def dublicate_order(self, order_id):
        item = self.order_rep.load_item(order_id)
        new_item = deepcopy(item)
        new_item.source_order_id=1
        new_item.ordered_status_id=10
        new_item.description_delivery="Одяг Jemis"
        new_item.order_code = self.generate_order_code()
        ordered_product = list(item.ordered_product)
        resp = self.add_order4(new_item)
        print("dublicate_order:", resp)
        if resp["add_order4"] == "ok":
            order = resp["result"]
            order = self.update_ordered_product(order.id, ordered_product)
            return order
        else:
            return False

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
    
    def search_order_6_number(self, data):
        return self.order_rep.search_for_all(data)

    def replace_phone(self, phone):
        return phone

    def parse_dict_status(self, data):
        orders = data["id"]
        status = data["status"]
        return orders, status
    
