import  re

class ParseText:
    def __init__(self):
        pass

    def parse_x(self, text): # парсер прихода цветов
        taken_text = re.findall(r'(\d+х-*\d+)', text)
        print(taken_text)
        data = {int(par.split('х')[0]): int(par.split('х')[1]) for par in taken_text}
        print(data)
        return data
    
    def parse_colon(self, text): # парсер прихода от курьера
        lines = text.strip().split("\n")  # Розбиваємо текст на рядки
        result = {"command": None, "comment": None, "items": []}

        command_match = re.match(r"#(\w+)\s+\(([^)]+)\):", lines[0])
        if command_match:
            result["command"] = command_match.group(1)  # Назва команди ("прихід")
            result["comment"] = command_match.group(2)  # Ім'я ("Игорь")

        for line in lines[1:]:  # Обробляємо кожен рядок після команди
            match = re.match(r"(\w+):\s*(\d+)\((\d+)\)", line)
            if match:
                result["items"].append({
                    "article": match.group(1),   # Артикул (45N10)
                    "quantity": int(match.group(2)),  # Кількість (20)
                    "total": int(match.group(3))  # Загальна сума (240)
                })
        return result
    
    
            
    def function_name(self):
        pass
        

# если ми вибираем команду то потом нужно провести манипуляции с текстом
# проблема углубления в количестве передачи данних