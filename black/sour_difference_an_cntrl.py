from a_service import SourDiffAnServ
from repository import SourDiffAnRep
from a_service import CacheService
from .work_time_cntrl import WorkTimeCntrl
from repository import OrderRep
from repository import ProductRep
from datetime import timedelta



class SourDiffAnCntrl():
    def __init__(self) -> None:
        self.sour_diff_an_rep = SourDiffAnRep()
        self.cache_serv = CacheService()
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
     
    def load_source_difference_id_period(self, id, period, days):
        start_time, stop_time = self.work_time_cntrl.load_work_time(period, days)
        product = self.sour_diff_an_rep.load_source_difference_id_period(
            id, start_time, stop_time
            )
        print(start_time, stop_time, "month")
        return product
    
    def load_source_diff_line(self, id):
        line = self.sour_diff_an_rep.load_source_diff_line(id)
        return line
    
    def load_source_diff_event_date(self, req):
        start, stop = self.sour_diff_an_serv.load_event_day(req)
        source = self.sour_diff_an_rep.load_source_difference_period(start, stop)
        return source 
    
    def load_last_line_id(self, id):
        source = self.sour_diff_an_rep.load_last_line_id(id) 
        return source
    
    
    def add_quantity_crm_today(self, products):
        print("Працюєм")
        event_date = next(self.work_time_cntrl.my_tgitпше ime()).strftime('%Y-%m-%d')
        # event_date = event_date - timedelta(days=1)
        # event_date = event_date.strftime('%Y-%m-%d')
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
 
    def add_line_comment(self, id, comment):
        return self.sour_diff_an_rep.add_diff_comment(id, comment)
    
    def update_source_difference(self, body):
        update = body
        return update
    
    def update_source_difference_period(self, period, days): # потрібно source_id 
        start_time, stop_time = self.work_time_cntrl.load_work_time(period, days)
        product = self.sour_diff_an_rep.load_source_difference_period(
            start_time, stop_time
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
    

    def delete_event_date(self, req):
        start, stop = self.sour_diff_an_serv.load_event_day(req)
        lines = self.sour_diff_an_rep.load_source_difference_period(start, stop)
        for line in lines:
            self.sour_diff_an_rep.delete_diff_line(line.id)
        return True

    
    def sour_diff_id_gone_list(self, id, period, days=None):
        start, stop = self.work_time_cntrl.load_work_time(period)
        print(start, " & ", stop)
        source_list = self.sour_diff_an_rep.load_source_difference_id_period(id, start, stop)
        print(source_list)
        self.sour_diff_an_serv.count_going_list(source_list, start, stop)
  
    
    def sour_diff_id_gone(self, id):
        start, stop = self.work_time_cntrl.load_work_time("days", 1)
        print(start, " & ", stop)
        old_source = self.sour_diff_an_rep.load_source_difference_id_period(id, start, stop)
        start, stop = self.work_time_cntrl.load_work_time("day")
        last_source = self.sour_diff_an_rep.load_source_difference_id_period(id, start, stop)
        quantity = self.sour_diff_an_serv.count_going(old_source, last_source)
        self.sour_diff_an_rep.update_source_diff_line_sold(id, quantity)
        print("last sold gone", quantity)
    
    def sour_diff_all_source_sold(self, source_all, period, days=None):
        for item in source_all:
            print(item.id, "item")
            self.sour_diff_id_gone_list(item.id, period, days)
        return True

    def delete(self, id):
        delete = self.sour_diff_an_rep.delete_diff_line(id)
        print("Видалено")
        return delete


 