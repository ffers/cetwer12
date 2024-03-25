from repository import ProductRep
from service_asx import ProductServ
from black import ProductAnaliticControl

prod_serv = ProductServ()
prod_rep = ProductRep()
analitic_cntrl = ProductAnaliticControl()

class ProductCntrl:
    def add_product(self, description, article, product_name, price, quantity):
        resp = prod_rep.add_product(description, article, product_name, price, quantity)
        return resp

    def load_product_all(self):
        resp = prod_rep.load_product_all()
        return resp

    def load_product_item(self, product_id):
        resp = prod_rep.load_product_item(product_id)
        return resp

    def update_product(self, req, id):
        update_data = prod_serv.update_product(req)
        resp_bool = prod_rep.update_product_item(update_data, id)
        if resp_bool:
            resp_analitic = analitic_cntrl.add_product_analitic(id)
            resp_update_money = analitic_cntrl.get_product_analitic(id)
        print(f"СМОТРИМ {update_data}")
        return resp_bool

    def update_after_arrival(self, combined_list):
        resp_bool = prod_rep.update_after_arrival(combined_list)
        return resp_bool



