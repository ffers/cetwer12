from repository import ProductRep
from a_service import ProductServ
from black import ProductAnaliticControl




class ProductCntrl:
    def __init__(self):
        self.an = ProductAnaliticControl()
        self.p_rep = ProductRep()
        self.p_serv = ProductServ()

    def add_product(self, description, article, product_name, price, quantity):
        resp = self.p_rep.add_product(description, article, product_name, price, quantity)
        return resp
    
    def add_product_relate(self, request):
        resp = False, "компонент не додано"
        list_data = self.p_serv.add_product_relate(request)
        for item in list_data:
            resp = self.p_rep.add_product_relate(item)
        return resp

    def update_product(self, req, id):
        update_data = self.p_serv.update_product(req)
        resp_bool = self.p_rep.update_product_item(update_data, id)
        if resp_bool:
            resp_analitic = self.an.add_product_analitic(id)
            resp_update_money = self.an.get_product_analitic(id)
        print(f"СМОТРИМ {update_data}")
        return resp_bool
     
    def update_prod_table(self, req):
        for item in req:
            id, serv = self.p_serv.update_prod_table(item)
            rep = self.p_rep.update_product_item(serv, id)
            if not rep:
                return False 
        return True

    def update_after_arrival(self, combined_list):
        resp_bool = self.p_rep.update_after_arrival(combined_list)
        return resp_bool

    def delete_product(self, id):
        bool = self.p_rep.delete_product(id)
        return bool

    def changeBodyPrice(self):
        self.p_rep.changeBodyPrice()
        return True


    def update_prod_relate(self, id, req):
        data = self.p_serv.add_product_relate(req)
        resp = self.p_rep.update_product_relate(*data, id)
        return resp
    
    def load_product_all(self):
        resp = self.p_rep.load_product_all()
        return resp

    def load_product_item(self, product_id):
        resp = self.p_rep.load_product_item(product_id)
        return resp
    
    def load_by_article(self, art):
        resp = self.p_rep.load_by_article(art)
        return resp

    def load_product_relate(self):
        data = self.p_rep.load_product_relate()
        return data

    def load_product_relate_item(self, product_id):
        item = self.p_rep.load_product_relate_item(product_id)
        return item
    def load_prod_relate_product_id_all(self, product_id):
        items = self.p_rep.load_prod_relate_product_id_all(product_id)
        return items

    def delete_product_relate(self, id):
        bool = self.p_rep.delete_product_relate(id)
        return bool

prod_cntrl = ProductCntrl()

