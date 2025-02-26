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
            match = re.match(r"(\w+):\s*(\d+)\((\d+)\)", line)
            if match:
                chat_data.content.append({
                    "article": match.group(1),   # Артикул (45N10)
                    "pack": int(match.group(2)),  # Кількість (20)
                    "quantity": int(match.group(3))  # Загальна сума (240)
                })
        return chat_data
    
    
            
    def parse_stock(self, chat_data):
        pass
        

# если ми вибираем команду то потом нужно провести манипуляции с текстом
# проблема углубления в количестве передачи данних