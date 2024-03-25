from repository import OrderRep

ord_rep = OrderRep()

class OrderCntrl:
    def dublicate(self, order_id):
        item = ord_rep.load_item(order_id)
        dublicate_item = ord_rep.dublicate_item(item)
        ord_prod_old = ord_rep.load_prod_order(order_id)
        dublicate_order_prod = ord_rep.dublicate_order_prod(dublicate_item, ord_prod_old)
        return True