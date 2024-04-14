



class ProductAnanaliticServ:
    def sum_money(self, body_price, quantity):
        print(f"ANALITIC_BOX {body_price} {quantity}")
        if not quantity:
            quantity = 0
        if not body_price:
            body_price = 0
        sum_money = body_price * quantity
        print(sum_money)
        return sum_money

    def count_sum(self, number_a, number_b):
        sum_resp = number_a * number_b
        return sum_resp



prod_an_serv = ProductAnanaliticServ()

