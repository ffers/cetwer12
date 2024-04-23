from .product_cntrl import prod_cntrl
from a_service import SourAnServ
from .jour_ch_cntrl import jour_ch_cntrl as journal
from .analitic_cntrl import an_cntrl
from repository import ord_rep
from datetime import datetime
from repository import sour_an_rep as rep
from .telegram_controller import tg_cntrl



class SourAnCntrl:
    def __init__(self):
        self.sour_an_serv = SourAnServ(prod_cntrl, journal, an_cntrl, rep, ord_rep)

    def my_time(self):
        yield (datetime.utcnow())

    def add(self, request):
        args = self.sour_an_serv.add_source(request)
        resp = rep.add_product_source(args)
        return resp

    def update(self, id, req):
        data = self.sour_an_serv.add_source(req)
        resp = rep.update_source(id, data)
        return resp

    def load_all(self):
        data = rep.load_all()
        return data

    def load_item(self, product_id):
        resp = rep.load_item(product_id)
        return resp

    def update_prod_sour_quan(self, id, quantity):
        resp = rep.update_quantity(id, quantity)
        return resp

    def load_article(self, article):
        item = rep.load_article(article)
        return item

    def delete(self, id):
        bool = rep.delete_(id)
        return bool

    def confirmed(self, order):
            resp = False
        # try:
            for product in order.ordered_product:
                prod_comps = prod_cntrl.load_prod_relate_product_id_all(product.product_id)
                if prod_comps:
                    for prod_comp in prod_comps:
                        if prod_comp:
                            sale_quantity = self.sour_an_serv.count_new_quantity(prod_comp, product)
                            resp = self.stock_journal(prod_comp.article, -sale_quantity)
                else:
                    resp_tg = f"Немає такого компоненту {product.products.article}"
                    tg_cntrl.sendMessage(tg_cntrl.chat_id_info, resp_tg)

            print(resp)
            return resp

    def add_arrival(self, req):
        list_data = self.sour_an_serv.add_arrival(req)
        resp = self.stock_journal(list_data[0], list_data[1])
        return resp

        # except Exception as e:
        #     resp = f"При рахувані исходника щось пішло не так: {e}"
        #     print(resp)
        #     return resp
    def stock_journal(self, article, quantity):
        resp = False
        prod_source = rep.load_article(article)
        if prod_source:
            new_quantity = self.sour_an_serv.new_qauntity(prod_source, quantity)
            resp = rep.update_quantity(prod_source.id, new_quantity)
            list_val = self.sour_an_serv.journal_func(prod_source, quantity)
            print(f"list_val {list_val}")
            resp = journal.add_(list_val)
        return resp

    def return_prod(self, order):
        resp = None
        for product in order.ordered_product:
            prod_comps = prod_cntrl.load_prod_relate_product_id_all(product.product_id)
            if prod_comps:
                for prod_comp in prod_comps:
                    sale_quantity = prod_comp.quantity * product.quantity
                    print(f"sale_quantity {sale_quantity}")
                    prod_source = rep.load_article(prod_comp.article)
                    new_quantity = prod_source.quantity + sale_quantity
                    print(f"new_quantity {new_quantity}")
                    resp = rep.update_quantity(prod_source.id, new_quantity)
                    prod_source = rep.load_article(prod_comp.article)
            else:
                resp = f"Немає такого компоненту {product.products.article}"
        return resp

    def all_analitic(self, orders, period):
        orders_quan = len(orders)
        torg_sum = self.sour_an_serv.torg_func(orders)
        body = self.sour_an_serv.body_func(orders)
        workers_mon = orders_quan * 27
        profit = torg_sum - body
        print(f"рахуєм: {orders_quan} {torg_sum} {body} {workers_mon} {profit}")
        resp = (torg_sum, body, workers_mon, 0.00, 0.00, 0.00, 0.00, profit, period, orders_quan)
        print(resp)
        return resp

    def work_analitic(self):
        balance = self.sour_an_serv.balance_func()
        wait = self.sour_an_serv.wait_func()
        stock = self.sour_an_serv.stock_func()
        inwork = self.sour_an_serv.inwork_func()
        salary = self.sour_an_serv.salary_func()
        income = self.sour_an_serv.income_func()
        return (balance, wait, stock, inwork, salary, income)

    def sort_send_time(self):
        resp = False
        orders = ord_rep.load_period_all()
        for order in orders:
            if not order.send_time:
                print("Щось оновлено")
                confirmed = self.confirmed(order)
                if confirmed:
                    ord_rep.update_time_send(order.id, next(self.my_time()))
                    resp = True, "Щось оновлено в искходниках"
            else:
                print("Є час в ордері")
        return resp


    def sort_analitic(self, period):
        resp = False, "Не спрацювало"
        self.sort_send_time()
        if period == "all":
            orders = ord_rep.load_period_all()
            item = an_cntrl.load_period(period)
            if item:
                data = self.all_analitic(orders, period)
                work_an = self.work_analitic()
                print(data+work_an)
                resp = an_cntrl.update_(item[0].id, data+work_an)
                return resp
            data = self.all_analitic(orders, period)
            work_an = self.work_analitic()
            resp = an_cntrl.add_(data + work_an)
        elif period == "day":
            print(period)
            orders = ord_rep.load_item_days()
            print(orders)
            item = an_cntrl.load_day()
            if item:
                data = self.all_analitic(orders, period)
                work_an = self.work_analitic()
                print(data + work_an)
                resp = an_cntrl.update_(item.id, data + work_an)
                return resp
            data = self.all_analitic(orders, period)
            work_an = self.work_analitic()
            resp = an_cntrl.add_(data + work_an)
        elif period == "week":
            item = an_cntrl.load_day()
            if item:
                resp = an_cntrl.update_(item.id, self.all_analitic(orders, period))
                return resp
            an_cntrl.add_(self.all_analitic(orders, period))
        elif period == "month":
            item = an_cntrl.load_day()
            if item:
                resp = an_cntrl.update_(item.id, self.all_analitic(orders, period))
                return resp
            resp = an_cntrl.add_(self.all_analitic(orders, period))
        return resp




sour_an_cntrl = SourAnCntrl()

# OrderProduct
# id = db.Column(db.Integer, primary_key=True)
# quantity = db.Column(db.Integer)
# price = db.Column(db.Float)
# order_id = db.Column(db.Integer, db.ForeignKey(
#     'orders.id', name='fk_ordered_product_order_id'), nullable=False)
# product_id = db.Column(db.Integer, db.ForeignKey(
#     'products.id', name='fk_ordered_product_product_id'))
# products = db.relationship('Pro


