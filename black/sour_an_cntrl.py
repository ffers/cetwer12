from .product_cntrl import prod_cntrl
from a_service import sour_an_serv


class SourAnCntrl:
    def confirmed(self, order):
        resp = None
        for product in order.ordered_product:
            prod_comps = prod_cntrl.load_prod_relate_product_id_all(product.product_id)
            if prod_comps:
                for prod_comp in prod_comps:
                    prod_source = prod_cntrl.load_product_source_article(prod_comp.article)
                    new_quantity = sour_an_serv.count_new_quantity(prod_comp, prod_source, product)
                    resp = prod_cntrl.update_prod_sour_quan(prod_source.id, new_quantity)
            else:
                resp = f"Немає такого компоненту {product.products.article}"
        return resp


    def return_prod(self, order):
        resp = None
        for product in order.ordered_product:
            prod_comps = prod_cntrl.load_prod_relate_product_id_all(product.product_id)
            if prod_comps:
                for prod_comp in prod_comps:
                    sale_quantity = prod_comp.quantity * product.quantity
                    print(f"sale_quantity {sale_quantity}")
                    prod_source = prod_cntrl.load_product_source_article(prod_comp.article)
                    new_quantity = prod_source.quantity + sale_quantity
                    print(f"new_quantity {new_quantity}")
                    resp = prod_cntrl.update_prod_sour_quan(prod_source.id, new_quantity)
            else:
                resp = f"Немає такого компоненту {product.products.article}"
        return resp

    def count_income(self, order):
        resp = True
        for product in order.ordered_product:
            prod_comps = prod_cntrl.load_prod_relate_product_id_all(product.product_id)
            if prod_comps:
                for prod_comp in prod_comps:
                    sale_quantity = prod_comp.quantity * product.quantity
                    print(sale_quantity)
                    prod_source = prod_cntrl.load_product_source_article(prod_comp.article)
                    body_price = prod_source.price * sale_quantity
                    # resp = prod_cntrl.update_prod_sour_quan(prod_source.id, mon_income)
                    print(f"mon_income: {body_price}")

            else:
                resp = False
        return resp


sour_an_cntrl = SourAnCntrl()

