from ..product_cntrl import prod_cntrl
from a_service import SourAnServ
from ..jour_ch_cntrl import jour_ch_cntrl as journal
from .analitic_table_cntrl import an_cntrl
from repository import ord_rep
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from ..telegram_controller import tg_cntrl
from black.work_time_cntrl import WorkTimeCntrl
from repository import SourceRep
from a_service import CacheService
from ..sour_difference_an_cntrl import SourDiffAnCntrl
from utils import my_time_v2

from utils import OC_logger

'''
Аналитика працює як окремий сервіс
якій кілька раз на день оновлює
свої данні
але данні по кількості інших параметрів таких як кількість 
джерел 

я завантажую спочатку за певний період ордери
потім починаю одразу рахувати и заносити це в кеш
мабуть потім записую в базу

я відталкуюсь від загального підрахунку 
как будто что тоо может измениться месяц назад
я думаю ничего не изменится существенного
по крайней мере можно внести правки в отдельние заметки
тоесть відштовхуватись потрібно за цей місяц
щоб поорахувати загальні суми треба відштовхуватись 
по рокам, таа останнім місяцям неділям, тижням
а зараз рахується по ордерам а не по вже аналітиці що є
если нет прошлого года то по и тд мес нед день ордер
пересчет ордеров можно делать за последние 2 месяца
после 1 числа будут изменения за пршлий месяц  
как делать изменения по дням неделям или месяцам 
добавить кол-во возвратов возврати можно считать за етот день
кажеться что можно считать день - сгоднешнее положение вещей
но когда ми считали раньше ми считали что получилось но ето 
потомучто сложно считать каждий день но в самом начале я считал и ето круто
week = дни за неделю
month = тижни сумма днів 
рік = місяці

'''
'''
оокей я хотів би додати вичет поо грошам на баланс але потім 
воно все перепише треюба подумати
мне нужен баланс
сейчас баланс ето деньги на карте
но мне  нужен баланс дохода и с него списивать затрати
а с зп списивать  затрати на другие вещи как зп налоги
тоесть с баланса списивать приход ето одно
а затрати с зп ето другое
но зп переписивааеться аналитикой
надо чтоби аналитика учитивала какие то сумми по зп скйчас ето 25462 в месяц
но также добавлять к етому какие то сумми 
то есть нужна таблица и страница редагування и модуль КРУД по ним
можно добавить сумму в код как тест но надо найти где в періоде
'''

'''
по приходу та уходу окрема графа тбто якщо прихд має бути флаг
а якшо уход інший флаг
варианта два 
или в момент прихода вичетать 
или в момент общего подсчета
'''

class SourAnCntrl:
    def __init__(self):
        self.w_time = WorkTimeCntrl()
        self.rep = SourceRep()
        self.sour_an_serv = SourAnServ(prod_cntrl,
                                       journal, an_cntrl,
                                       self.rep, ord_rep, self.w_time)
        self.cash = CacheService()
        self.sour_an_diff_cntrl = SourDiffAnCntrl()
        self.logger = OC_logger.oc_log('sour_an_cntrl.analitic')

    def my_time(self):
        yield datetime.now(timezone.utc)

    def time_period_utc(self, period):
        start_time, stop_time = self.w_time.load_work_time(period)
        start_utc = start_time.replace(tzinfo=timezone.utc)
        end_utc = stop_time.replace(tzinfo=timezone.utc)
        return start_utc, end_utc


    def add(self, request):
        args = self.sour_an_serv.add_source(request)
        resp = self.rep.add_product_source(args)
        return resp
    
    def add_quantity_crm_today(self):
        sources = self.load_all()
        add = self.sour_an_diff_cntrl.add_quantity_crm_today(sources)
        return add
    
    def add_comment_diff(self, source_id, comment, new_quantity):
        last_line = self.sour_an_diff_cntrl.load_last_line_id(source_id)
        print("загрузили last_line")
        update = self.sour_an_diff_cntrl.add_line_comment(last_line.id, comment)

        update_quantity_crm = self.sour_an_diff_cntrl.update_quantity_crm([[last_line.id, new_quantity]])
        print(update_quantity_crm, " update_quantity_crm")
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
        resp = self.rep.update_source(id, data)
        return resp

    def load_all(self):
        data = self.rep.load_all()
        return data

    def load_item(self, product_id):
        resp = self.rep.load_item(product_id)
        return resp

    def load_article(self, article):
        item = self.rep.load_article(article)
        return item

    def get_search(self, req):
        result = self.sour_an_serv.get_search(req)
        return result

    def update_prod_sour_quan(self, id, quantity):
        resp = self.rep.update_quantity(id, quantity)
        return resp

    def delete(self, id):
        bool = self.rep.delete_(id)
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
            return True
        return False
      
    def fixed_process(self, source_id, sale_quantity, description, event_date=None): # получает компонент не имеет а из прихода отправляю
        journal = self.stock_journal(source_id, sale_quantity, description, event_date)
        comment_diff = self.add_comment_diff(source_id, description + f': {sale_quantity}.', journal[1])
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
        prod_source = self.rep.load_item(prod_sourc_id)
        if prod_source:
            new_quantity = self.sour_an_serv.new_qauntity(prod_source, quantity)
            resp = self.rep.update_quantity(prod_source.id, new_quantity)
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
            income = self.cash.income_func(self.rep.load_article("income"))
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
        print("period:", period)
        self.sort_send_time()
        start_time, stop_time = self.w_time.load_work_time(period)
        print(start_time, ' ', stop_time)
        self.logger.debug(f"period: {start_time, stop_time}")
        print(f"period: {start_time, stop_time}")
        'остановился здесь'
        # остановился здесь 
        orders = ord_rep.load_period(start_time, stop_time)
        print(orders)
        item = an_cntrl.load_period_sec(period, start_time, stop_time) 
        # переіод нужен если ми считаем все 
        # получить все = считаем день берем все и добавляєм вчерашний день 
        # но что то меняється за два месяца... будем считать на сегодняшний день и прогноз
        if item:
            print(f"update {item}")
            resp = self.update_analitic(orders, item, period)
            return resp
        print("add")
        data = self.first_an(orders, period)
        resp_first = an_cntrl.add_first(data)
        self.logger.debug(f"resp_first: {resp_first}")
        self.logger.debug(f'item: {period, start_time, stop_time}')
        print(f"period: {period, start_time, stop_time}")
        item = an_cntrl.load_period_sec(period, start_time, stop_time)
        self.logger.debug(f'item: {item}')
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


