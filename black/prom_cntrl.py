

import os, re


class PromCntrl:
    def send_ttn(self, order_id, invoice_n, delivery, evo_cl):
        order_id = re.sub(r"\D", "", order_id)
        env = os.getenv("ENV")
        if env != "dev":
            resp = evo_cl.send_ttn(order_id, invoice_n, delivery)
            return resp
        return {"success": "dev"}
    
    def change_status(self, order_id, status, evo_cl):
        order_id = re.sub(r"\D", "", order_id)
        env = os.getenv("ENV")
        if env != "dev":
            resp = evo_cl.change_status(order_id, status)
            return resp
        return {"success": "dev"}

