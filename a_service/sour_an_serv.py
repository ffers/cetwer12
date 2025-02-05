from decimal import Decimal
from itertools import zip_longest


class SourAnServ:
    def __init__(self, prod_cntrl, journal, an_cntrl, rep_sour, ord_rep, w_time_cntrl):
        self.prod_cntrl = prod_cntrl
        self.journal = journal
        self.an_cntrl = an_cntrl
        self.rep = rep_sour
        self.ord_rep = ord_rep
        self.w_time_cntrl = w_time_cntrl

    def format_float(self, num):
        try:
            if isinstance(num, int):
                num_format = str(f"{int(num)}.00")
                # Конвертуємо int у Decimal
                return Decimal(num_format)
            else:
                num_format = float(num)
                # Конвертуємо float у Decimal
                return Decimal(str(f"{num_format: .2f}"))
        except ValueError:
            return None

    def add_source(self, request):
        print("add_product_source")
        article = request.form['article']
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        money = self.format_float(price) * int(quantity)
        list_data = [article, name, price, quantity, money]
        print(list_data)
        return list_data

    def add_arrival(self, req):
        print(req.form)
        article = req.form.getlist('article')
        description = req.form.getlist('description')
        quantity = req.form.getlist('quantity')
        event_date = req.form.getlist('event_date')
        combined_list = list(zip_longest(article, quantity, description, event_date, fillvalue=event_date[0]))
        print(combined_list)
        return combined_list        
         
    def get_search(self, req):
        search_query = req.args.get('q', '').lower()
        items = self.rep.load_all()
        result = []
        for item in items:
            if search_query in item.article.lower() or search_query in item.name.lower():
                prod_data = {
                    'id': item.id,
                    'article': item.article + ' - ' + item.name
                }
                result.append(prod_data)
        return result


    def count_new_quantity(self, prod_comp, product):
        sale_quantity = prod_comp.quantity * product.quantity
        return sale_quantity

    def new_qauntity(self, prod_source, sale_quantity):
        new_quantity = prod_source.quantity + sale_quantity
        return new_quantity

    def journal_func(self, prod_source, sale_quantity, description, event_date):
        body = prod_source.price * sale_quantity
        quantity_stock = prod_source.quantity
        print(quantity_stock)
        return description, sale_quantity, body, prod_source.id, quantity_stock, event_date

    def torg(self, product):
        torg = 0
        if product.quantity and product.price:
            torg = product.quantity * product.price
        return torg


    def torg_func(self, orders):
        torg_sum = 0
        for order in orders:
            for product in order.ordered_product:
                torg_sum += self.torg(product)
        return torg_sum

    def body(self, prod_comp, prod_source, product):
        sale_quantity = prod_comp.quantity * product.quantity
        print(f"prod_source.name {prod_source.name}")
        body = prod_source.price * sale_quantity
        return body
    
    def body_func(self, orders):
        body = 0
        for order in orders:
            for product in order.ordered_product:
                prod_comps = self.prod_cntrl.load_prod_relate_product_id_all(product.product_id)
                # print("Ищем prod_comps")
                if prod_comps:
                    # print("Нашли prod_comps")
                    for prod_comp in prod_comps:
                        try:
                            print(prod_comp)
                            prod_source = self.rep.load_id(prod_comp.product_source_id)
                            if prod_source:
                                body += self.body(prod_comp, prod_source, product)
                        except Exception as e:
                            print(f"Помилка загрузки body_func: {e}")
                else:
                    resp = False
        return body

    def cpa_com_f(self, orders):
        cpa_commission = 0
        for order in orders:
            if order.cpa_commission:
                cpa_commission += self.format_float(order.cpa_commission)
        return cpa_commission

    def rozet_f(self, orders):
        rozet = 0
        for order in orders:
            if order.delivery_method_id == 2:
                print(order.delivery_method.name)
                rozet += 30
        return rozet

    def definetion_prod(self, order):
        resp = {
            "ok": [],
            "info": []
        }
        for product in order.ordered_product:
            prod_comps = self.prod_cntrl.load_prod_relate_product_id_all(product.product_id)
            if prod_comps:
                resp["ok"].append(True)
            else:
                resp["ok"].append(False)
                resp["info"].append(f"{order.order_code}: {product.products.article}")
        print(resp)
        return resp

    def profit_f(self):
        profit = 0
        items = self.an_cntrl.load_all()
        for item in items:
            profit += item.torg - item.body
        return profit








