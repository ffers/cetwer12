from decimal import Decimal
from itertools import zip_longest
from repository import ProductRep, ProductAnaliticRep
from utils import OC_logger
'''
продукт сервіс 
нужно иметь виду аналитику каждое действие должно бить с ней связано 
думаю нужно виполнять здесь все необходимое чтоби вернуть готовий продукт
тоесть ордер создает заказ потом просит продукт 
аналитика добавляється к продукту при создании продукта
аналитика проводится отдельним путем но изменения которие происходят должни идти 
через продакт аналитику
когда виполняється ордер процесс какой либо затрагиваеться аналитика в том числе
пока что аналитика происходит чудообразом но надо будет переформатировать
мои модули слишком взаимо связани зотя в моем случає нужно 
писать микросервиси
пока что кажеться обработка ордеров самий тяжелий процесс
также аналитика
и все таки при создании товара может необходимо передать в аналитику о новом товаре
но кто должен ето делать
координатор процеесов заказа или склад
думаю склад должен делать свою аналитику а ордер свою
'''

class ProductServ:
    def __init__(self):
        self.prod_rep = ProductRep()
        self.prod_an_rep = ProductAnaliticRep()
        self.log = OC_logger.oc_log('product_serv')

    def add_product_v2(self, article, product_name):
        product =  self.prod_rep.create_v2(article, product_name)
        if product:
            self.add_product_anltc(product.id)
        return product
    
    def update_v2(self, id, *args):
        print("update_v2", args)
        product =  self.prod_rep.update_v2(id, *args)
        return product
    
    def add_product_anltc(self, product_id):
        return self.prod_an_rep.add_product_analitic(product_id)

    def format_float(self, num):
        try:
            if isinstance(num, int):
                num_format = str(f"{int(num)}.00")
                # Конвертуємо int у Decimal
                return Decimal(num_format)
            else:
                num_format = float(num)
                # Конвертуємо float у Decimal
                return Decimal(str(f"{num_format: .2f}"))
        except ValueError:
            return None

    def update_product(self, req):
        article = req.form['article']
        product_name = req.form['product_name']
        description = req.form['description']
        input_value = req.form['quantity']
        body_product_price_draft = req.form["body_product_price"]
        body_product_price = self.format_float(body_product_price_draft)
        if input_value:
            quantity = int(input_value)
        else:
            quantity = 0
        price_ch = req.form['price']
        print(price_ch)
        price = self.format_float(price_ch)
        print(price, product_name)
        return (article, product_name, description, quantity, price, body_product_price)
    
    def update_prod_table(self, row):
        line_id = [row["article"], row["name"]]
        print(line_id)
        return int(row["id"]), line_id

    def add_product_relate(self, req):
        print(f"Компоненти {req.form}")
        print("add_product_relate")
        name = ""
        article = req.form.getlist('article')
        quantity = req.form.getlist('quantity')
        product_id = req.form.getlist('product')
        combined_list = list(zip_longest(article, quantity, product_id, fillvalue=None))
        return combined_list
 
    def load_item_by_article(self, artcl, name="Перевірити назву"):
        print(f"load_item_by_article {self}")
        try:
            product = self.prod_rep.load_by_article(artcl)
            if not product:
                product = self.add_product_v2(artcl, name)
            return product
        except Exception as e:
            self.log.error(f'load_item_by_article: {e} self meaning: {self}')
            raise
    
    def load_item_id(self, id):
        return self.prod_rep.load_product_item(id)

    def load_all(self):
        return self.prod_rep.load_product_all()
  
    def create_data_relate_req(self, req):
        data = [
            req.form["product"],
            req.form["name"],
            req.form["article"],
            req.form["quantity"]
        ]
        return data

    def create_data_source_req(self, req):
        data = [
            req.form["article"],
            req.form["name"],
            req.form["price"],
            req.form["quantity"]
        ]
        return data



prod_serv = ProductServ()