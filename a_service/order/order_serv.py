import random
from flask import jsonify

class OrderServ:
    def generate_order_code(self, prefix='ASX'):
        digits = [random.choice('0123456789') for _ in range(6)]
        unique_id = ''.join(digits)  # Генеруємо унікальний ID та беремо перші 6 символів
        order_code = f'{prefix}-{unique_id}'
        return order_code

    # def examine_code(self, order, code):
    #     while True:
    #           # Генеруємо нове значення
    #         if not order:  # Перевіряємо, чи таке значення ще не використовувалось
    #             used_values.add(new_digits)  # Додаємо нове значення до множини використаних
    #             return new_digits  # Повертаємо унікальне значення

    def search_for_order(self, order):
        order_list = []
        if order:
            for item in order:
                if item.order_id_sources:
                    item_data = self.create_text(item)
                    order_list.append(item_data)
                    print(order_list)
            return jsonify({'results': order_list})
        return jsonify({'results': []})


    def create_text(self, item):
        product_text = ' '
        for product in item.ordered_product:
            product_text += product.products.article + ' '
        text = (item.order_id_sources + ' '
                + item.client_lastname + ' '
                + item.client_firstname + ' '
                + product_text + ' ')
        item_data = {
            'id': item.id,
            'text': text
        }
        return item_data

    def replace_phone(self, phone):
        return phone

    def parse_dict_status(self, data):
        orders = data["id"]
        status = data["status"]
        return orders, status



