



class ProductAnanaliticServ:
    def sum_money(self, body_price, quantity):
        print(f"ANALITIC_BOX {body_price} {quantity}")
        if not quantity:
            quantity = 0
        sum_money = body_price * quantity
        print(sum_money)
        return sum_money      



