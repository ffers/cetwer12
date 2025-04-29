
#  id |        name        | description
# ----+--------------------+-------------
#   1 | Підтвердити        |
#   2 | Підтвержено        |
#   3 | Оплачено           |
#   4 | Несплачено         |
#   5 | Скасовано          |
#   6 | Предзамовлення     |
#   7 | Питання            |
#   8 | Відправлено        |
#   9 | Отримано           |
#  10 | Нове               |
#  11 | Очікує відправленя |
#  12 | Виконано           |
#  13 | Тест
#  14 | Повернення
#  15 | Редагування


'''
Дуже потужно працюʼє цепочка обовʼязків
'''

class Handler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler
        

    def handle(self, repo, list_order):
        context = self.process(repo)
        list_order.extend(context)
        if self.next_handler:
            return self.next_handler.handle(repo, list_order)
        return list_order

    def process(self, repo):
        raise NotImplementedError("Override process() in subclass")

class New(Handler):
    def process(self, repo):
        orders = repo.load_status_id(10)
        return orders
        
class Paid(Handler):
    def process(self, repo):
        orders = repo.load_status_id(3)
        return orders

class Unpaid(Handler):
    def process(self, repo):
        orders = repo.load_status_id(4)
        return orders

class Editing(Handler):
    def process(self, repo):
        orders = repo.load_status_id(1)
        return orders

class StatusNewWithPaidPipline:
    def __init__(self):
        self.pipeline = New(
                Paid(
                    Unpaid(
                        Editing()
                    )
                )
        )

    def process(self, repo):
        list_order = []
        result = self.pipeline.handle(repo, list_order)
        print("\nРезультат виконання:", "✅ Успішно" if result else "❌ Помилка")
        return result