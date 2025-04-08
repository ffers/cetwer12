


from datetime import datetime




class Order:
    def __init__(self, order_id, status, tg_cntrl, tg_serv, ord_rep):
        self.order_id = order_id
        self.status = 10
        self.created_at = datetime.now()
        self.tg_cntrl = tg_cntrl()
        self.tg_serv = tg_serv()
        self.ord_rep = ord_rep()

    def process(self):
        raise NotImplementedError("Subclasses must implement process()")