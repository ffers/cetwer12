import  re

class ParseText:
    def __init__(self):
        pass

    def parse_x(self, chat_data): # парсер прихода цветов
        text = chat_data.text
        taken_text = re.findall(r'(\d+х-*\d+)', text)
        print(taken_text)
        data = {int(par.split('х')[0]): int(par.split('х')[1]) for par in taken_text}
        print(data)
        return data
    
    def parse_colon(self, chat_data): # парсер прихода от курьера
        text = chat_data.text
        lines = text.strip().split("\n")  # Розбиваємо текст на рядки
        command_match = re.match(r"#(\w+)\s+\(([^)]+)\):", lines[0])
        if command_match:
            chat_data.comment = command_match.group(2)+"\n"  # Ім'я ("Игорь")
        chat_data.content = []
        for line in lines[1:]:  # Обробляємо кожен рядок після команди
            print("line;", line)
            match = re.search(r"(\w+):\s*(\d+)\s*\((\d+)\)", line)
            print("match:", match)
            if match:
                chat_data = self.parse_colon_true(chat_data, match)
        return chat_data
    
    def parse_colon_true(self, chat_data, match):
        quantity = self.quantity_parse(chat_data, match)
        chat_data.content.append({
                    "article": match.group(1),   # Артикул (45N10)
                    "pack": int(match.group(2)),  # Кількість (20)
                    "quantity": quantity  # Загальна сума (240)
                })
        return chat_data
    
    def quantity_parse(self, chat_data, match):
        quantity = int(match.group(3))
        if chat_data.cmd == "take": 
            return -quantity
        return quantity
    
    
    
    def search_order_code(self, text):
        pattern = r'Замовлення № (\S+)'
        number_order = re.search(pattern, text)
        print(number_order)
        return number_order.group(1).strip()
    
    def search_6_number(self, text):
        patterns = [
            r"ASX-\d{6,}",
            r"R-\d{6,}",
            r"P-\d{6,}",
            r"\b\d{9}\b"
        ]

        combined = "|".join(patterns)
        regex = re.compile(combined)

        matches = regex.findall(text)
        return matches[0] if matches else False

    
    
            
    def parse_stock(self, chat_data):
        pass
        

# если ми вибираем команду то потом нужно провести манипуляции с текстом
# проблема углубления в количестве передачи данних