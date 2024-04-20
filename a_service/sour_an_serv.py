
class SourAnServ:
    def count_new_quantity(self, prod_comp, prod_source, product):
        sale_quantity = prod_comp.quantity * product.quantity
        new_quantity = prod_source.quantity - sale_quantity
        return new_quantity

    def body_price(self, a, b, c):
        sale_quantity = a.quantity * b.quantity
        resp = c.price * sale_quantity
        return resp

sour_an_serv = SourAnServ()