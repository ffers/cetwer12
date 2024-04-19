
class SourAnServ:
    def count_new_quantity(self, prod_comp, prod_source, product):
        sale_quantity = prod_comp.quantity * product.quantity
        new_quantity = prod_source.quantity - sale_quantity
        return new_quantity

sour_an_serv = SourAnServ()