


class Parse:
    def __init__(self):
        pass

    def all_color(self, items):
        sum = 0
        for a,b in items.items():
            sum += b
        return sum
    
    def quantity_parse(self, item):
        if "data" in item:
            return self.all_color(item["data"])
        return item["quantity"]

    def parser_item(self, data_chat, article, quantity):
        data_chat.resp.append({
            "article": article,
            "quantity": quantity
        })
        return data_chat
