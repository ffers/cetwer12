from a_service import SourDiffAnServ
from repository import SourDiffAnRep
from a_service import CacheService
from .sour_an_cntrl import SourAnCntrl
from .work_time_cntrl import WorkTimeCntrl



class SourDiffAnCntrl():
    def __init__(self) -> None:
        self.sour_diff_an_serv = SourDiffAnServ()
        self.sour_diff_an_rep = SourDiffAnRep()
        self.cache_serv = CacheService()
        self.sour_an_cntrl = SourAnCntrl()
        self.work_time_cntrl = WorkTimeCntrl()

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
        product = self.sour_an_cntrl.load_all()
        event_date = next(self.work_time_cntrl.my_time()).strftime('%Y-%m-%d')
        for item in product:
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
    
    def update_source_difference_id_period(self, id, start_time, stop_time):
        product = self.sour_diff_an_rep.load_source_difference_id_period(
            id, start_time, stop_time
            )
         
        quantity_crm = self.cache_serv.set("sour_diff_available", product.available)
        item = self.sour_an_cntrl.load_item(id)
        quantity_stock = self.cache_serv.set("sour_diff_stock", item.quantity)

        difference = self.cache_serv.get("sour_diff_available") - self.cache_serv.get("sour_diff_stock")
        return product
    
    def update_source_diff_line(self, req, id):
        args_obj = self.sour_diff_an_serv.update_source_diff_line(req)
        term = self.sour_diff_an_rep.update_source_diff_line(args_obj, id)
        return term