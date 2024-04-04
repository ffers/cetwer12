from service_asx.analitic import ProductAnanaliticServ
from repository import ProductAnaliticRep

prod_an_rep = ProductAnaliticRep()

pr_an_serv = ProductAnanaliticServ()

class ProductAnaliticControl():
    def sum_money_in_product(self, product_id):
        body_price = prod_an_rep.body_product_price(product_id)
        quantity = prod_an_rep.quantity_product(product_id)
        sum_money = pr_an_serv.sum_money(body_price, quantity)
        return sum_money

    def sum_quantity_sale(self, product_id):
        sum_quantity_sale = prod_an_rep.get_sum_product_sale(product_id)
        print(f"Quantity product sale {sum_quantity_sale}")
        return sum_quantity_sale

    def money_in_sale(self, product_id):
        body_price = prod_an_rep.body_product_price(product_id)
        quantity_sale = prod_an_rep.get_sum_product_sale(product_id)
        sum_money = pr_an_serv.sum_money(body_price, quantity_sale)
        return sum_money

    def item_product_analitic(self, product_id):
        item_product_analitic = prod_an_rep.item_product_analitic(product_id)
        print(f"Money in product1 {item_product_analitic.money_in_product}")
        return item_product_analitic

    def all_product_analitic(self):
        all_item = prod_an_rep.all_product_analitic()
        return all_item

    def add_product_analitic(self, product_id):
        prod_item = prod_an_rep.search_an_product_id(product_id)
        if not prod_item:
            prod_an_rep.add_product_analitic(product_id)
            return True
        return False

    def get_product_analitic(self, product_id):
        prod_item = prod_an_rep.search_an_product_id(product_id)
        if prod_item:
            resp_bool_money = self.update_product_analitic(product_id)
            return resp_bool_money
        return False

    def update_product_analitic(self, product_id):
        sum_money = self.sum_money_in_product(product_id)
        sum_quantity_sale = self.sum_quantity_sale(product_id)
        money_in_sale = self.money_in_sale(product_id)
        resp_bool = prod_an_rep.update_product_analitic(
            product_id,
            sum_money,
            sum_quantity_sale,
            money_in_sale
            )
        return resp_bool

    def day_analitic(self):
        pass

    def product_in_order(self, order):
        for product in order.ordered_product:
            self.add_product_analitic(product.product_idx   )
            self.get_product_analitic(product.product_id)
        return True







