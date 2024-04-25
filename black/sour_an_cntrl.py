from .product_cntrl import prod_cntrl
from a_service import SourAnServ
from .jour_ch_cntrl import jour_ch_cntrl as journal
from .analitic_cntrl import an_cntrl
from repository import ord_rep
from datetime import datetime
from repository import sour_an_rep as rep
from .telegram_controller import tg_cntrl
from .work_time_cntrl import WorkTimeCntrl


class SourAnCntrl:
    def __init__(self):
        self.w_time_cntrl = WorkTimeCntrl()
        self.sour_an_serv = SourAnServ(prod_cntrl,
                                       journal, an_cntrl,
                                       rep, ord_rep, self.w_time_cntrl)

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

    def load_article(self, article):
        item = rep.load_article(article)
        return item

    def get_search(self, req):
        result = self.sour_an_serv.get_search(req)
        return result

    def update_prod_sour_quan(self, id, quantity):
        resp = rep.update_quantity(id, quantity)
        return resp

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
                            description = order.order_id_sources + ' ' + product.products.article
                            sale_quantity = self.sour_an_serv.count_new_quantity(prod_comp, product)
                            resp = self.stock_journal(prod_comp.article, -sale_quantity, description)
                else:
                    resp_tg = f"Немає такого компоненту {product.products.article}"
                    tg_cntrl.sendMessage(tg_cntrl.chat_id_info, resp_tg)

            print(resp)
            return resp

    def add_arrival(self, req):
        list_data = self.sour_an_serv.add_arrival(req)
        resp = self.stock_journal(list_data[0], list_data[1], list_data[2])
        resp_an = self.sort_analitic("all")
        return resp

        # except Exception as e:
        #     resp = f"При рахувані исходника щось пішло не так: {e}"
        #     print(resp)
        #     return resp
    def stock_journal(self, article, quantity, description):
        resp = False
        prod_source = rep.load_article(article)
        if prod_source:
            new_quantity = self.sour_an_serv.new_qauntity(prod_source, quantity)
            resp = rep.update_quantity(prod_source.id, new_quantity)
            list_val = self.sour_an_serv.journal_func(prod_source, quantity, description)
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

    def first_an(self, orders, period):
        orders_quan = len(orders)
        torg_sum = self.sour_an_serv.torg_func(orders)
        body = self.sour_an_serv.body_func(orders)
        workers_mon = orders_quan * 27
        profit = torg_sum - body
        cpa_com = self.sour_an_serv.cpa_com_f(orders)
        rozet = self.sour_an_serv.rozet_f(orders)
        print(f"рахуєм: {orders_quan} {torg_sum} {body} {workers_mon} {profit} {cpa_com}")
        resp = (torg_sum, body, workers_mon, cpa_com, rozet, 0.00, 0.00, profit, period, orders_quan)
        print(resp)
        return resp

    def work_analitic(self):
        balance = self.sour_an_serv.balance_func()
        wait = self.sour_an_serv.wait_func()
        stock = self.sour_an_serv.stock_func()
        inwork = self.sour_an_serv.inwork_func()
        income = self.sour_an_serv.income_func()
        return (balance, wait, stock, inwork, income)

    def salary_f(self, period):
        salary = self.sour_an_serv.salary_func(period)
        return salary

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


    def update_analitic(self, orders, item, period):
        data = self.first_an(orders, period)
        resp = an_cntrl.update_(item.id, data)
        work_an = self.work_analitic()
        print(work_an)
        resp_work = an_cntrl.update_work(item.id, work_an)
        print(resp_work)
        salary = self.salary_f(period)
        resp_salary = an_cntrl.update_salary(item.id, salary)
        print(resp_salary)
        return resp




    def sort_analitic(self, period):
        resp = False, "Не спрацювало"
        print(period)
        self.sort_send_time()
        start_time, stop_time = self.w_time_cntrl.load_work_time(period)
        print(start_time,' ', stop_time)
        orders = ord_rep.load_period(start_time, stop_time)
        print(orders)
        item = an_cntrl.load_period_sec(period, start_time, stop_time)
        if item:
            # item = item
            print(f"update {item}")
            resp = self.update_analitic(orders, item, period)
            return resp
        print("add")
        data = self.first_an(orders, period)
        resp_first = an_cntrl.add_first(data)
        print(resp_first)
        item = an_cntrl.load_period_sec(period, start_time, stop_time)
        resp = self.update_analitic(orders, item, period)
        return resp
        # if period == "day":
        #     orders = ord_rep.load_item_days()
        #     print(orders)
        #     item = an_cntrl.load_period(period)[0]
        #     if item:
        #         data = self.first_an(orders, period)
        #         resp = an_cntrl.update_(item.id, data)
        #         work_an = self.work_analitic()
        #         resp_work = an_cntrl.update_work(item.id, work_an)
        #         print(work_an)
        #         salary = self.salary_f(period)
        #         resp_salary = an_cntrl.update_salary(item.id, salary)
        #         return resp
        #     data = self.first_an(orders, period)
        #     resp_first = an_cntrl.add_first(data)
        # elif period == "week":
        #     orders = ord_rep.load_item_days()
        #     item = an_cntrl.load_day()
        #     if item:
        #         data = self.first_an(orders, period)
        #         resp = an_cntrl.update_(item.id, data)
        #         work_an = self.work_analitic(period)
        #         resp_work = an_cntrl.update_work(item.id, work_an)
        #         return resp
        #     data = self.first_an(orders, period)
        #     work_an = self.work_analitic(period)
        #     resp_first = an_cntrl.add_first(data)
        #     resp_work = an_cntrl.add_work_an(work_an)
        # elif period == "month":
        #     orders = ord_rep.load_item_days()
        #     item = an_cntrl.load_day()
        #     if item:
        #         data = self.first_an(orders, period)
        #         work_an = self.work_analitic(period)
        #         resp = an_cntrl.update_(item.id, data)
        #         resp_work = an_cntrl.update_work(item.id, work_an)
        #         return resp
        #     data = self.first_an(orders, period)
        #     work_an = self.work_analitic(period)
        #     resp_first = an_cntrl.add_first(data)
        #     resp_work = an_cntrl.add_work_an(work_an)
        #




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


