from repository import WorkSpaceRep



class WorkSpaceServ:
    def __init__(self):
        self.work_space_rep = WorkSpaceRep()

    def load_payment_methods(self):
        return self.work_space_rep.load_payment_methods()
    
    def load_delivery_methods(self):
        return self.work_space_rep.load_delivery_methods()
    
    def load_sources_order(self):
        return self.work_space_rep.load_sources_order()
    