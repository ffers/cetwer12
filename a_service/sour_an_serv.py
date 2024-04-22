
class SourAnServ:
    def __init__(self, prod_cntrl, journal, an_cntrl, rep, ord_rep):
        self.prod_cntrl = prod_cntrl
        self.journal = journal
        self.an_cntrl = an_cntrl
        self.rep = rep
        self.ord_rep = ord_rep

    def count_new_quantity(self, prod_comp, prod_source, product):
        sale_quantity = prod_comp.quantity * product.quantity
        new_quantity = prod_source.quantity - sale_quantity
        return new_quantity

    def journal_func(self, prod_comp, prod_source, product):
        sale_quantity = prod_comp.quantity * product.quantity
        body = prod_source.price * sale_quantity
        quantity_stock = prod_source.quantity
        print(quantity_stock)
        return "-", sale_quantity, body, prod_source.id, quantity_stock

    def torg(self, product):
        torg = 0
        if product.quantity and product.price:
            torg = product.quantity * product.price
        return torg

    def body(self, prod_comp, prod_source, product):
        sale_quantity = prod_comp.quantity * product.quantity
        body = prod_source.price * sale_quantity
        return body

    def torg_func(self, orders):
        torg_sum = 0
        for order in orders:
            for product in order.ordered_product:
                torg_sum += self.torg(product)
        return torg_sum

    def body_func(self, orders):
        body = 0
        for order in orders:
            for product in order.ordered_product:
                prod_comps = self.prod_cntrl.load_prod_relate_product_id_all(product.product_id)
                if prod_comps:
                    for prod_comp in prod_comps:
                        try:
                            prod_source = self.prod_cntrl.load_product_source_article(prod_comp.article)
                            if prod_source:
                                body += self.body(prod_comp, prod_source, product)
                        except Exception as e:
                            print(f"Помилка загрузки body_func: {e}")
                else:
                    resp = False
        return body

    def balance_func(self):
        balance = 0
        items = self.an_cntrl.load_period("all")
        for item in items:
            if item.income:
                print(item.income)
                balance += item.income
            else:
                balance += 0
        return balance

    def wait_func(self):
        orders = self.ord_rep.load_period_all()
        wait = self.torg_func(orders)
        items = self.an_cntrl.load_period("all")
        for item in items:
            if item.income:
                wait -= item.income
            else:
                wait -= 0
        return wait

    def stock_func(self):
        stock = 0
        items = self.prod_cntrl.load_product_source_all()
        for item in items:
            stock += item.money
        return stock

    def inwork_func(self):
        income = 0
        items = self.an_cntrl.load_all()
        # for item in items:
        #     income += item.wait + item.stock + item.balance

        return income

    def salary_func(self):
        salary = 0
        items = self.an_cntrl.load_all()
        for item in items:
            salary += item.profit - item.worker \
            - item.prom - item.rozet - item.insta
        return salary

    def income_func(self):
        resp = self.rep.load_article("income")
        return resp.money





