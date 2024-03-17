from repository import AnaliticRep

anrep_cl = AnaliticRep()

class ProductAnanaliticServ:
    def main(self, product_id):
        resp = self.sum_money_in_product(product_id)
        return resp

    def sum_product_quantity_order(self, product_id):
        sum_item = anrep_cl.sum_product_quantity_order(product_id)

    def sum_money_in_product(self, product_id):
        body_price = anrep_cl.body_product_price(product_id)
        quantity = anrep_cl.quantity_product(product_id)
        print(f"ANALITIC_BOX {body_price} {quantity}")
        sum_money = body_price * quantity
        return sum_money



