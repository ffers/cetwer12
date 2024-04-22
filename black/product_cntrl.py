from repository import prod_rep
from a_service import prod_serv
from black import ProductAnaliticControl

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

    def delete_product(self, id):
        bool = prod_rep.delete_product(id)
        return bool

    def changeBodyPrice(self):
        prod_rep.changeBodyPrice()
        return True

    # relate product

    def add_product_relate(self, request):
        args = prod_serv.add_product_relate(request)
        resp = prod_rep.add_product_relate(args)
        return resp

    def update_prod_relate(self, id, req):
        data = prod_serv.add_product_relate(req)
        resp = prod_rep.update_product_relate(data, id)
        return resp

    def load_product_relate(self):
        data = prod_rep.load_product_relate()
        return data

    def load_product_relate_item(self, product_id):
        item = prod_rep.load_product_relate_item(product_id)
        return item
    def load_prod_relate_product_id_all(self, product_id):
        items = prod_rep.load_prod_relate_product_id_all(product_id)
        return items

    def delete_product_relate(self, id):
        bool = prod_rep.delete_product_relate(id)
        return bool







prod_cntrl = ProductCntrl()

