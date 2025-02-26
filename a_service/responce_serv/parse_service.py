


class Parse:
    def __init__(self):
        pass

    def all_color(self, items):
        sum = 0
        for a,b in items.items():
            sum += b
        return sum

    def article(self, data):
        return data["size"] + "N"

    def count_sum(self, data):
        pass