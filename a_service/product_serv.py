from decimal import Decimal
from itertools import zip_longest
from repository import ProductRep

class ProductServ:
    def __init__(self):
        self.prod_rep = ProductRep()

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
    
    def load_item_by_article(self, artcl):
        return self.prod_rep.load_by_article(artcl)
    
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