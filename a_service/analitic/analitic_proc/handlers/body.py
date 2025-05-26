from ...base import Handler
from utils import DEBUG

class ComponetnsNotConnect(Exception):
    pass

class Body(Handler):
    def process(self, order):
        body_dict = self.body_dict(order)
        print('DEBUG', DEBUG)
        if DEBUG > 4: print('body_dict:', body_dict)
        return self.count_body(body_dict)
        

    def body_dict(self, order):
        resp = {'resp': []}
        for product in order.ordered_product:
            try:
                resp['resp'].append(self.start(product))
            except Exception as e:
                self.ctx.logger.exception(f'body_dict: {e}')
                resp['resp'].append({
                    'product': product.products.article,
                    'body':0
                                })
                if DEBUG >= 3: print('Помилка підрахунку')
        return resp  
        
    def start(self, product):
        prod_comps = self.load_related(product)
        return {
            'product': product.products.article,
            'body': self.load_component(prod_comps, product)
                        }


    def load_related(self, product):
        components = self.ctx.prod_rep.load_prod_relate_product_id_all(product.product_id)
        if DEBUG > 5: print('components:', components)
        if not components:
            self.logger.info(f'Нема компонента для {product.article}')
            'треба ще відправити в тг повідомленя'
            raise ComponetnsNotConnect('Ненайдени компоненти')
        return components

    def load_component(self, prod_comps, product):
        body = 0
        for compt in prod_comps:
            try:
                if DEBUG > 5: print(compt)
                source = self.ctx.source_rep.load_id(compt.product_source_id)
                if DEBUG > 5: print('load_component:', source)
                if source:
                    body += self.body(compt, source, product)
            except Exception as e:
                print(f"Помилка загрузки body_func: {e}")
        return body

    def body(self, prod_comp, prod_source, product):
        sale_quantity = prod_comp.quantity * product.quantity
        if DEBUG > 5: print(f"prod_source.name {prod_source.name}")
        body = prod_source.price * sale_quantity
        return body

    def count_body(self, body_dict):
        body = 0
        for item in body_dict['resp']:
            if DEBUG > 5: print('count_body:', item)
            body += item['body']
        return body