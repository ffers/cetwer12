



class TestJournal:
    def __init__(self):
        pass

    def check_components(self, order):
        comps_bool = self.sour_an_serv.definetion_prod(order)
        if all(comps_bool['ok']):
            return True
        else:
            resp_tg = f"Немає такого компоненту {comps_bool['info']}"
            tg_cntrl.sendMessage(tg_cntrl.chat_id_info, resp_tg)
            return False
        
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