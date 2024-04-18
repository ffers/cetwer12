from .product_cntrl import prod_cntrl
from a_service import sour_an_serv


class SourAnCntrl:
    def confirmed(self, order):
        for product in order.ordered_product:
            prod_comps = prod_cntrl.load_prod_relate_product_id_all(product.product_id)
            if prod_comps:
                for prod_comp in prod_comps:
                    sale_quantity = prod_comp.quantity * product.quantity
                    prod_source = prod_cntrl.load_product_source_article(prod_comp.article)
                    new_quantity = prod_source.quantity - sale_quantity
                    resp = prod_cntrl.update_prod_sour_quan(prod_source.id, new_quantity)
        return resp


    def return_prod(self, order):
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
        return resp


sour_an_cntrl = SourAnCntrl()

