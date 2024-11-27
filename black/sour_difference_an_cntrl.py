from a_service import SourDiffAnServ
from repository import SourDiffAnRep
from a_service import CacheService
from .sour_an_cntrl import SourAnCntrl
from .work_time_cntrl import WorkTimeCntrl
from repository import OrderRep
from repository import ProductRep




class SourDiffAnCntrl():
    def __init__(self) -> None:
        self.sour_diff_an_rep = SourDiffAnRep()
        self.cache_serv = CacheService()
        self.sour_an_cntrl = SourAnCntrl()
        self.work_time_cntrl = WorkTimeCntrl()
        self.ord_rep = OrderRep()
        self.prod_rep = ProductRep()
        self.sour_diff_an_serv = SourDiffAnServ(
            self.cache_serv, 
            self.sour_diff_an_rep,
            self.prod_rep
            )

    def load_source_difference(self):
        product = self.sour_diff_an_rep.load_source_difference() 
        return product
     
    def load_source_difference_id_period(self, id, period):
        start_time, stop_time = self.work_time_cntrl.load_work_time(period)
        product = self.sour_diff_an_rep.load_source_difference_id_period(
            id, start_time, stop_time
            )
        return product
    
    def load_source_diff_line(self, id):
        line = self.sour_diff_an_rep.load_source_diff_line(id)
        return line
    
    
    def add_quantity_crm_today(self):
        print("Працюєм")
        products = self.sour_an_cntrl.load_all()
        event_date = next(self.work_time_cntrl.my_time()).strftime('%Y-%m-%d')
        start, stop = self.work_time_cntrl.load_work_time("all")
        orders = self.ord_rep.load_period(start, stop)
        sold_quantities = self.sour_diff_an_serv.source_diff_sold_optimized(orders, products)
        for item in products:
            data = self.sour_diff_an_serv.add_quantity_crm(item, event_date)
            update = self.sour_diff_an_rep.add_quantity_crm(data)
        return update
            


    def add_source_difference_req(self, req):
        args_obj = self.sour_diff_an_serv.add_source_difference_req(req)
        print(args_obj)
        bool_obj = self.sour_diff_an_rep.add_source_difference(args_obj)
        return bool_obj
    
    def add_source_difference_scr(self, req):
        args_obj = self.sour_diff_an_serv.add_source_difference_req(req)
        print(args_obj)
        bool_obj = self.sour_diff_an_rep.add_source_difference(args_obj)
        return bool_obj

    def update_source_difference(self, body):
        update = body
        return update
    
    def update_source_difference_id_period(self, id, period): # потрібно source_id 
        start_time, stop_time = self.work_time_cntrl.load_work_time(period)
        product = self.sour_diff_an_rep.load_source_difference_id_period(
            id, start_time, stop_time
            )
        diff_sum = self.sour_diff_an_serv.source_difference_sum(product)
        return product
    
    def update_source_diff_line(self, req, id):
        args_obj = self.sour_diff_an_serv.update_source_diff_line(req)
        line = self.sour_diff_an_rep.update_source_diff_line(args_obj, id)
        return line
    
    def update_sour_diff_table(self, data):
        list_data = self.sour_diff_an_serv.update_sour_diff_table(data)
        add = self.sour_diff_an_rep.update_diff_table(list_data)
        return add
    
    def sour_diff_id_gone(self, id):
        start, stop = self.work_time_cntrl.load_work_time("days", 1)
        print(start, " & ", stop)
        old_source = self.sour_diff_an_rep.load_source_difference_id_period(id, start, stop)
        start, stop = self.work_time_cntrl.load_work_time("day")
        last_source = self.sour_diff_an_rep.load_source_difference_id_period(id, start, stop)
        quantity = self.sour_diff_an_serv.count_going(old_source, last_source)
        self.sour_diff_an_rep.update_source_diff_line_sold(id, quantity)
        print("last sold gone", quantity)