import  re

class ParseText:
    def __init__(self):
        pass

    def parse_text(self, text):
        taken_text = re.findall(r'(\d+х-*\d+)', text)
        print(taken_text)
        # pars = taken_text.split(', ')
        data = {int(par.split('х')[0]): int(par.split('х')[1]) for par in taken_text}
        print(data)
        return data