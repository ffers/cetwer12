from utils import BearRequest


class Parser:
    def payment_status(self, order, flag):
        print(f"flag {flag}")
        if flag == "canceled":
            order.ordered_status_id = 5
        elif flag == "paid":
            order.payment_status_id = 1
            order.ordered_status_id = 3
        elif flag == "unpaid":
            order.payment_status_id = 2
            order.ordered_status_id = 4
        elif flag == "refunded":
            order.ordered_status_id = 5
            order.payment_status_id = 3

