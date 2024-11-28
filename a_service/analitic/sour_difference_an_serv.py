from datetime import datetime, timezone, timedelta
import time







class SourDiffAnServ():
    def __init__(self, cache_serv, sour_diff_an_rep, prod_rep) -> None:
        self.cache_serv = cache_serv
        self.sour_diff_an_rep = sour_diff_an_rep
        self.prod_rep = prod_rep

    def add_source_difference_req(self, req):
        event_date = datetime.strptime(req.form['event_date'], "%d-%m-%Y")
        source_id = req.form['source_id']
        quantity_crm = req.form['quantity_crm']
        quantity_stock = req.form['quantity_stock']
        difference = req.form['difference']
        return (event_date, source_id, quantity_crm,  
                quantity_stock, difference)
    
    def update_quantity(self, products):
        for product in products:
            product.quantity

    def update_sour_diff_table(self, data):
        line_id = []
        for row in data:
            if row["stock"] == "None":
                row["stock"] = 0
            line_id.append([int(row["id"]), int(row["stock"])])
        print(line_id)
        return line_id
 
    def add_quantity_crm(self, item, event_date):
        quantity = item.quantity
        id = item.id
        data = (event_date, id, quantity)
        return data
    
    def update_source_diff_line(self, req):
        quantity_crm = req.form['quantity_crm']
        quantity_stock = req.form['quantity_stock']
        return ( quantity_crm,  
                quantity_stock)
    
    def load_event_day(self, req):
        start = datetime.strptime(req.form['event_date_start'], "%d-%m-%Y")
        stop = datetime.strptime(req.form['event_date_stop'], "%d-%m-%Y")
        return start, stop
       
    def source_difference_sum(self, product):
        if product:
            for item in product:
                if item.quantity_crm and item.quantity_stock:
                    source_difference = item.quantity_stock - item.quantity_crm
                    add_cache = self.cache_serv.set("source_difference", source_difference)
                    print(self.cache_serv.get("source_difference"))
                    update = self.sour_diff_an_rep.update_diff_sum(self.cache_serv.get("source_difference"), item.id)  
            return True
        return False
    
    def source_diff_sold(self, orders, item):
        quantity = 0
        for order in orders:
            comps_bool = self.sour_an_serv.definetion_prod(order)
            if all(comps_bool):
                for product in order.ordered_product:
                    prod_comps = prod_cntrl.load_prod_relate_product_id_all(product.product_id)
                    for prod_comp in prod_comps:
                        if item == prod_comp:
                            print(f"prod_comps {prod_comps}")
                            sale_quantity = prod_comp.quantity * product.quantity
                            return sale_quantity
                        

    def source_diff_sold_optimized(self, orders, sources):
        # Кешуємо відповідності товарів та компонентів
        prod_to_comps = {}
        for source in sources:
            prod_to_comps[source] = self.prod_rep.load_prod_relate_product_id_all(source.id) 
            print(f"Проверка 1 {prod_to_comps}")
            print(f"Проверка 2 {sources}")
        # Підраховуємо кількість проданих компонентів
        sold_quantities = {item: 0 for item in sources}
        for order in orders:
            if all(self.definetion_prod(order)):
                for product in order.ordered_product:
                    
                    if product.product_id in prod_to_comps:
                        print(f"Є продакт_айди {prod_to_comps} {product.product_id}")
                        for comp in prod_to_comps[product.product_id]:
                            if comp in sold_quantities:
                                print(f"Є кількість {comp} {sold_quantities}")
                                sold_quantities[comp] += comp.quantity * product.quantity
        print( f"Кількість: {sold_quantities}")
        return sold_quantities
    
    def definetion_prod(self, order):
        resp = {
            "ok": [],
            "info": []
        }
        for product in order.ordered_product:
            prod_comps = self.prod_rep.load_prod_relate_product_id_all(product.product_id)
            if prod_comps:
                resp["ok"].append(True)
            else:
                resp["ok"].append(False)
                resp["info"].append(f"{order.order_code}: {product.products.article}")
        return resp
    
    def count_going(self, old_source, last_source):
        send = []
        if old_source and last_source:
            print(old_source[0].quantity_crm, " old_source ")
            print(last_source[0].quantity_crm, " last_source ")
            sum = old_source[0].quantity_crm - last_source[0].quantity_crm

            print(sum, "sum")
            return sum
        else:
            print("source None")
            return 0
        
    def count_going_list(self, source_list, start, stop):
        for line in source_list: # проходим по всем строкам продукта
            search_time = line.event_date - timedelta(days=1) # для етой строки вичислиям день до етого
            # print(line.event_date, "line.event_date", search_time)
            search = False; count = 0
            # print(line.id)
            count_diff = stop - start
            print(count_diff, "count_diff")
            while not search and count < count_diff.days: # проходим пока не найдем день
                time.sleep(1)
                count += 1
                print(count, "count")
                # print(search_time, " search_time ")
                search = self.search_day(source_list, search_time, line)
                if not search:
                    search_time = search_time - timedelta(days=1)

    def search_day(self, source_list, search_time, line):
        for line_old in source_list: # опять проходимся по строкам 
            # print()
            # print(line_old.event_date, "line_old.event_date", line.event_date, "event_date")
            if search_time == line_old.event_date: # если находим дату на день раньше
                quantity = line.quantity_crm - line_old.quantity_crm
                print(quantity, "quantity")
                self.sour_diff_an_rep.update_source_diff_line_sold(quantity, line.id)
                return True 
        self.sour_diff_an_rep.update_source_diff_line_sold(0, line.id)
        return False
                    #проходим по списку если ненашли соотвующий день минусуем еще день
                    
