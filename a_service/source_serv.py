from repository import SourceRep

from utils import wrapper, OC_logger



'''
проблема в таблице 
идет кол-во и деньги тоесть изменяємие параметри
при изменение исходника пристуствуют ети параметри и не понятно что с ними делать 
можноо ли их изменять прямо в апдейт или толькко через приходи 
и уходи
пока оставлю так но ето нужно менять
при постановке на приход по новому исходнику видно 
что идет связь с таблицей исходниками разници
появляється строитель или обсервер 
когда добавить нужен строитель 
когда удалить или изменить также наверное
вообще ничего нельзя делать без таблици разници иначе будут неправельние
параиметри
'''

'''
немогу воспринять что нужно делать очень крупний модуль когда козалось би
такие простие действия 
но нужно логирование
нужно ответ view
нужно обрабативвать ошибки
плюс ето дает возможность легко масштабироввать и понимать
что ето модуль
и будет держать в рамках куда двигаться
и опять же я столкнулся с тем что мне нужно передать
ошибку но я немогу ее передать 
последовательность не позволяет
но рейс можно виполнить в diffcntrl
тогда весь код сводится к ожной функции
по факту если не использоовать False в базе а передавать ошибку
то не нужна проверка на False + сразу знаем ошибку
опять застрял с форматом передачи данних
использовал стратегию но не зашло вернулся к builder
теперь самое смешное что нужно ли ето или достаточно 5 строчек кода
def build(self, data, Diff):
    rep = SourceRep()
    diff = Diff()

    data = rep.create_v2(data)
    diff.add_quantity_crm_today([data])

    return data

конечно етот код не расширяєм але меня бентежить
що процесс з іншою таблицєю
а фактично це проста функція create але вона не прста бо працює 
ще аналітіка
треба рообити мікросервіси але як сповіщати що треба щось робити 
мені це нагадує звісно обсервер якій при зміні повідомляє іншим 
якщо є потреба кілька сервісів сповістити 
то можливо треба обсервер як от ордер обсервер
'''

class Handler:
    def __init__(self, Diff):
        self.diff = Diff()
        self.rep = SourceRep()

    def execute(self, data):
        pass

class CreateHandler(Handler):
    def execute(self, data):
        print("CreateHandler", data)
        data = self.rep.create_v2(data)
        return data

class AddDiffHandler(Handler):
    def execute(self, data):
        sources = [data]
        print("AddDiffHandler:", sources)
        self.diff.add_quantity_crm_today(sources)  
        return data


class SourceServ:
    def __init__(self):
        self.commands = [
            CreateHandler,
            AddDiffHandler 
            ] 

    def add_command(self, command_class):
        self.commands.append(command_class)
        return self

    def build(self, pointer, Diff):  
            for cmd_class in self.commands:
                print("Працює: ", cmd_class.__name__)
                pointer = cmd_class(Diff).execute(pointer)
            return pointer
    
    # def stock_journal(self, prod_sourc_id, quantity, description, event_date=None):
    #     resp = False
    #     new_quantity = 0
    #     prod_source = self.rep.load_item(prod_sourc_id)
    #     if prod_source:
    #         new_quantity = prod_source.quantity - quantity
    #         resp = self.rep.update_quantity(prod_source.id, new_quantity)
    #         list_val = self.sour_an_serv.journal_func(prod_source, quantity, description, event_date)
    #         print(f"list_val {list_val}")
    #         resp = journal.add_(list_val)
    #     return resp, new_quantity
    

