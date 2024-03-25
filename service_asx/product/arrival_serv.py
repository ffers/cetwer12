from itertools import zip_longest
from decimal import Decimal
from datetime import datetime

class ArrivalServ:
    def add_arrival(self, request):
        resp_tuple = self.get_req_arr(request)
        combined_list = list(zip_longest(resp_tuple[0],
                resp_tuple[1], resp_tuple[2], resp_tuple[3], resp_tuple[4], fillvalue=None))
        print(f"combined_list {combined_list}")
        return combined_list

    def get_req_arr(self, request):
        datetime_new = list(datetime.strptime(request.form['event_date'], "%d-%m-%Y") for item in request.form.getlist('product'))
        product_id = list(int(item) for item in request.form.getlist('product'))
        quantity = list(int(item) for item in  request.form.getlist('quantity'))
        price = [self.format_decimal(item) for item in request.form.getlist('price')]
        total = [self.format_decimal(item) for item in request.form.getlist('total')]
        print(f"get_req_arr {datetime_new}, {product_id}, {quantity}, {price}, {total}")
        return (datetime_new, product_id, quantity, price, total)

    def format_decimal(self, num):
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

