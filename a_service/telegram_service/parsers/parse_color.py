import re

from dataclasses import dataclass

@dataclass
class ParseData:
    cmd: str = None
    content: list = None
    resp: list = None


class TextColorParser():

    def parse_text(self, text):
        taken_text = re.findall(r'(\d+х-*\d+)', text)
        print(taken_text)
        data = {int(par.split('х')[0]): int(par.split('х')[1]) for par in taken_text}
        print(data)
        return data

    def count_flag(self, text):
        if "#взял" in text:
            return "#взял"
        if "#склад" in text:
            return "#склад"
        if "#редактируєм" in text:
            return "#склад"

    def count_size(self, text):
        if "45:" in text:
            return "45N"
        if "35:" in text:
            return "35N"
        if "35:" in text and "45:" in text:
            return "two_size"
        

    def responce_text(self, data, size):
        text = f"{size}\n"
        for item in data:
            text += f"{item.color}х{item.quantity}, "
        return text

    def exect_text(self, text):
            data35_and_45 = re.search(r'35:(.*?45:|$)', text, re.DOTALL)
            data45 = re.findall(r'45:(.*?)(?:\d+х-*\d+:|$)', text, re.DOTALL)
            return data35_and_45[0], data45[0]


    def crete_two(self, text):
        data35, data45 = self.exect_text(text)
        clean_35 = self.parse_text(data35)
        clean_45 = self.parse_text(data45)
        print(f" 35 {clean_35}")
        print(f" 45 {clean_45}")
        return clean_35, clean_45

    def count_all(self, data): 
        count = 0
        for item in data:
             count += item.quantity
        return count
        
    def manager_bot(self, chat_data):
        text = chat_data.text
        if "35:" in text or "45:" in text:
            print("ПРАЦЮЄ")
            data = self.parse_text(text)
            # try:
            if "35:" in text and "45:" in text:
                size = self.count_size(text)
                clean_35, clean_45 = self.crete_two(text)
                print("Ось вийшло два розміри")
                print(clean_35)
                print(clean_45)
                chat_data.content = [{"article": "35", "data":clean_35}]
                chat_data.content.append({"article": "45", "data":clean_45})
            else:
                print(data)
                size = self.count_size(text)
                print(f"ОСЬ ВИЙШЛО {data, size}")
                chat_data.content = [{"article": size, "data":data}]
            return chat_data
            # except:
            #     return "Неправильно сформульоване повідомлення"



