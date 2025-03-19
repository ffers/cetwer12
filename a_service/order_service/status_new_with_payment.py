
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




class Handler:
    list_order = []
    
    def __init__(self, next_handler=None):
        self.next_handler = next_handler
        

    def handle(self, repo):
        context = self.process(repo)
        if self.next_handler:
            self.list_order.extend(context)
            print(f"handle: {self.list_order}")
            return self.next_handler.handle(repo)
        return self.list_order

    def process(self, repo):
        raise NotImplementedError("Override process() in subclass")

class New(Handler):
    def process(self, repo):
        resp = repo.load_status_id(10)
        print(resp)
        return resp
        
class Paid(Handler):
    def process(self, repo):
        resp = repo.load_status_id(3)
        print(resp)
        return resp

class Unpaid(Handler):
    def process(self, repo):
        resp = repo.load_status_id(4)
        print(resp)
        return resp

class StatusNewWithPaidPipline:
    def __init__(self):
        self.pipeline = New(
                Paid(
                    Unpaid()
                )
        )

    def process(self, repo):
        result = self.pipeline.handle(repo)
        print("\nРезультат виконання:", "✅ Успішно" if result else "❌ Помилка")
        return result