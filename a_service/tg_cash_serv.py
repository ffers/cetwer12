import re


class TgArrivalServ:
    def __init__(self):
        pass
    def article(self, text):
        taken_text = self.parse(text)
        if taken_text:
            data_dict = self.data_f(taken_text)
            return data_dict
        else:
            return False

    def parse(self, text):
        taken_text = re.findall(r'(\w+=-*\d+=\w+)', text)
        print(taken_text)
        # pars = taken_text.split(', ')
        # data = {par.split('=')[0]: int(par.split('=')[1]) for par in taken_text}
        # print(data)
        return taken_text

    def data_f(self, items):
        data_dict = []
        for item in items:
            data_dict.append({
                "article": item.split('=')[0],
                "quantity": item.split('=')[1],
                "description": "Приход " + item.split('=')[2]
            })
        # print(data_dict)
        return data_dict
