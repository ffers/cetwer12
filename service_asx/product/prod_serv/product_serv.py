from decimal import Decimal


class ProductServ:
    def format_float(self, num):
        try:
            if isinstance(num, int):
                num_format = str(f"{int(num)}.00")
                # Конвертуємо int у Decimal
                return Decimal(num_format)
            else:
                num_format = float(num)
                # Конвертуємо float у Decimal
                return Decimal(str(f"{num_format: .2f}"))
        except ValueError:
            return None

    def update_product(self, req):
        article = req.form['article']
        product_name = req.form['product_name']
        description = req.form['description']
        input_value = req.form['quantity']
        body_product_price_draft = req.form["body_product_price"]
        body_product_price = self.format_float(body_product_price_draft)
        if input_value:
            quantity = int(input_value)
        else:
            quantity = None
        price_ch = req.form['price']
        print(price_ch)
        price = self.format_float(price_ch)
        print(price, product_name)
        return (article, product_name, description, quantity, price, body_product_price)
