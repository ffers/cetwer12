import re


class TgCashServ:
    def __init__(self):
        pass
    def arrival(self, text):
        taken_text = self.parse(text)
        if taken_text:
            data_dict = self.data_f(taken_text)
            return data_dict
        else:
            return False

    def quan_f(self, text):
        parse_quan = self.parse_quan(text)
        articles = self.data_quan(parse_quan)
        return articles

    def parse_quan(self, text):
        taken_text = re.findall(r'#quan (.*)', text)
        print(taken_text)
        pars = taken_text[0].split(', ')
        print(pars)
        return pars
    def parse(self, text):
        taken_text = re.findall(r'(\w+=-*\d+=\w+)', text)
        print(taken_text)
        # pars = taken_text.split(', ')
        # data = {par.split('=')[0]: int(par.split('=')[1]) for par in taken_text}
        # print(data)
        return taken_text

    def data_quan(self, items):
        data_dict = []
        for item in items:
            data_dict.append({
                "article": item
            })
        print(data_dict)
        return data_dict

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
