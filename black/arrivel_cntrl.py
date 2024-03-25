from repository import ArrivalRep
from itertools import zip_longest
from service_asx.product import ArrivalServ
from black.product_cntrl import ProductCntrl
from black.product_analitic_cntrl import ProductAnaliticControl

arr_serv = ArrivalServ()
arr_rep = ArrivalRep()
prod_cntrl = ProductCntrl()
pr_analit_cntrl = ProductAnaliticControl()


class ArrivelCntrl:
    def add_arrival(self, request):
        combined_list = arr_serv.add_arrival(request)
        resp_bool = arr_rep.add_arrival(combined_list)
        resp_bool = prod_cntrl.update_after_arrival(combined_list)
        resp_bool = self.update_product_analitic(combined_list)
        return resp_bool

    def update_product_analitic(self, combined_list):
        for item in combined_list:
            product_id = item[1]
            pr_analit_cntrl.update_product_analitic(product_id)
        return True

    def load_all_arrival(self):
        arrival = arr_rep.load_arrival()
        return arrival




