from .product_cntrl import prod_cntrl
from a_service import SourAnServ
from .jour_ch_cntrl import jour_ch_cntrl as journal
from .analitic_cntrl import an_cntrl
from repository import ord_rep
from datetime import datetime
from repository import sour_an_rep as rep
from .telegram_controller import tg_cntrl
from .work_time_cntrl import WorkTimeCntrl
from repository import SourAnRep
from a_service import CacheService
from .sour_difference_an_cntrl import SourDiffAnCntrl

class SourAnCntrl:
    def __init__(self):
        self.w_time_cntrl = WorkTimeCntrl()
        self.sour_an_serv = SourAnServ(prod_cntrl,
                                       journal, an_cntrl,
                                       rep, ord_rep, self.w_time_cntrl)
        self.rep = SourAnRep()
        self.cash = CacheService()
        self.sour_an_diff_cntrl = SourDiffAnCntrl()

    def my_time(self):
        yield (datetime.now())

    def add(self, request):
        args = self.sour_an_serv.add_source(request)
        resp = rep.add_product_source(args)
        return resp
    
    def add_quantity_crm_today(self):
        sources = self.load_all()
        add = self.sour_an_diff_cntrl.add_quantity_crm_today(sources)
        return add
    
    def add_comment_diff(self, source_id, comment):
        last_line = self.sour_an_diff_cntrl.load_last_line_id(source_id)
        print("загрузили last_line")
        update = self.sour_an_diff_cntrl.add_line_comment(last_line.id, comment)
        return update
    
    def add_arrival(self, req):
        list_data = self.sour_an_serv.add_arrival(req)
        for item in list_data:
            print(f"item list_data{item}")
            resp = self.fixed_process(item[0], int(item[1]), item[2], datetime.strptime(item[3], "%d-%m-%Y"))
            # у меня есть source_id, надо найти в артикул и последнюю запись
            # добавить коментарий 
        # resp_an = self.sort_analitic("all")
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
        return self.prod_component_process(order, action_type='confirmed')
    
    def return_prod(self, order):
        return self.prod_component_process(order, action_type='return')
    
    def prod_component_process(self, order, action_type):
        if self.check_components(order):
            for product in order.ordered_product:
                prod_comps = prod_cntrl.load_prod_relate_product_id_all(product.product_id)
                for prod_comp in prod_comps:
                    sale_quantity, description = self.get_action_prod_component(prod_comp, product, order, action_type) 
                    print(sale_quantity, ' ', description, "prod_component_process")    
                    curent_time = next(self.my_time())           
                    if sale_quantity and description:
                        print('fixed_process')
                        self.fixed_process(prod_comp.product_source.id, sale_quantity, description, curent_time)
                    else:
                        return False
        return True
      
    def fixed_process(self, source_id, sale_quantity, description, event_date=None): # получает компонент не имеет а из прихода отправляю
        journal = self.stock_journal(source_id, sale_quantity, description, event_date)
        comment_diff = self.add_comment_diff(source_id, description + f': {sale_quantity}')
        print(journal, comment_diff, 'fixed_process')
        return comment_diff
        
    def get_action_prod_component(self, prod_comp, product, order, action_type): 
        # Визначає конкретний тип дії.
        if action_type == 'return':
            return prod_comp.quantity * product.quantity, f"Возврат: {order.order_code}, {product.products.article}"
        elif action_type == 'confirmed':
            sale_quantity = self.sour_an_serv.count_new_quantity(prod_comp, product)
            return -sale_quantity, f"{order.order_code} {product.products.article}"
        else:
            # Невідомий тип дії
            return None, None
    
    def check_components(self, order):
        comps_bool = self.sour_an_serv.definetion_prod(order)
        if all(comps_bool['ok']):
            return True
        else:
            resp_tg = f"Немає такого компоненту {comps_bool['info']}"
            tg_cntrl.sendMessage(tg_cntrl.chat_id_info, resp_tg)
            return False

    def update_all_analitic(self):
        self.sort_analitic("all")
        self.sort_analitic("year")
        self.sort_analitic("month")
        self.sort_analitic("week")
        self.sort_analitic("day")
        return True

    def stock_journal(self, prod_sourc_id, quantity, description, event_date=None):
        resp = False
        new_quantity = 0
        prod_source = rep.load_item(prod_sourc_id)
        if prod_source:
            new_quantity = self.sour_an_serv.new_qauntity(prod_source, quantity)
            resp = rep.update_quantity(prod_source.id, new_quantity)
            list_val = self.sour_an_serv.journal_func(prod_source, quantity, description, event_date)
            print(f"list_val {list_val}")
            resp = journal.add_(list_val)
        return resp, new_quantity
    
     
 
    def first_an(self, orders, period):
        orders_quan = len(orders)
        torg_sum = self.sour_an_serv.torg_func(orders)
        body = self.sour_an_serv.body_func(orders)
        workers_mon = orders_quan * 27
        profit = torg_sum - body
        cpa_com = self.sour_an_serv.cpa_com_f(orders)
        rozet = self.sour_an_serv.rozet_f(orders)
        print(f"рахуєм: {orders_quan} {torg_sum} {body} {workers_mon} {profit} {cpa_com}")
        resp = (torg_sum, body, workers_mon, cpa_com, rozet, 0, 0, profit, period, orders_quan)
        self.cash.create_set(resp)
        print(f"итого кеш: {self.cash.get_all()}")
        return resp

    def work_analitic(self, period):
        if period == "all":
            stock = self.cash.stock_func(self.load_all())
            income = self.cash.income_func(rep.load_article("income"))
            balance = self.cash.balance_func(self.rep.load_article("balance"))
            wait = self.cash.wait_func()
            inwork = self.cash.inwork_func()
            data = (balance, wait, stock, inwork, income)
        else:
            stock = self.cash.get("stock")
            income = self.cash.get("income")
            balance = self.cash.get("balance")
            wait = self.cash.get("wait")
            inwork = self.cash.get("inwork")
            data = (balance, wait, stock, inwork, income)
        return data

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
                    print(resp[1])
        return resp


    def update_analitic(self, orders, item, period):
        data = self.first_an(orders, period)
        resp = an_cntrl.update_(item.id, data)
        work_an = self.work_analitic(period)
        print(work_an)
        resp_work = an_cntrl.update_work(item.id, work_an)
        print(resp_work)
        salary = self.cash.salary_func()
        resp_salary = an_cntrl.update_salary(item.id, salary)
        print(resp_salary)
        return resp


 

    def sort_analitic(self, period):
        resp = False, "Не спрацювало"
        print(period)
        self.sort_send_time()
        start_time, stop_time = self.w_time_cntrl.load_work_time(period)
        print(start_time, ' ', stop_time)
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
    
    def source_sum_sold(self, source, sale_quantity): # получаем sold и добавляєм в кеш по исходнику
        sum_sold = self.cash.get("source_{}".format(source.id))
        if not sum_sold:
            data = self.cash.set("source_{}".format(source.id), sale_quantity)  # и тут либо сразу в базу либо в кеш а потом в базу
        else:
            new_sum = sum_sold + sale_quantity
            update = self.cash.set("source_{}".format(source.id), new_sum)

    def sour_diff_all_source_sold(self, period, days=None):
        source_all = self.load_all()
        sold = self.sour_an_diff_cntrl.sour_diff_all_source_sold(source_all, period, days)
        return sold
    



        
        




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


