from server_flask.db import db
from server_flask.models import Colorrep35, Colorrep45
from flask import current_app
import re


class ProductCounBot():
    def parse_text(self, text):
        taken_text = re.findall(r'(\d+х-*\d+)', text)
        print(taken_text)
        # pars = taken_text.split(', ')
        data = {int(par.split('х')[0]): int(par.split('х')[1]) for par in taken_text}
        print(data)
        return data

    def create_datebase(self, name_tabl):
        # Створення словника з номерами і кількістю
        database = {number: 0 for number in range(1, 28)}
        with current_app.app_context():
            for number, quantity in database.items():
                print(f"ДОДАЄМ {number, quantity}")
                color = name_tabl.query.filter_by(color=number).first()
                if not color:
                    data = name_tabl(color=number, quantity=quantity)
                    db.session.add(data)
            db.session.commit()

    def add_to_base(self, taken_data, name_tabl):
        with current_app.app_context():
            for number, quantity in taken_data.items():
                print(f"ДОДАЄМ {number, quantity}")
                data = name_tabl(color=number, quantity=quantity)
                db.session.add(data)
                db.session.commit()
            db.session.commit()

    def update_base(self, taken_data, name_tabl, flag):
        with current_app.app_context():
            for number, quantity in taken_data.items():
                print(f"ДОДАЄМ {number, quantity}")
                color = name_tabl.query.filter_by(color=number).first()
                if color:
                    if flag == "#взял":
                        color.quantity -= quantity
                    if flag == "#склад":
                        color.quantity += quantity
                    db.session.add(color)
            db.session.commit()

    def see_update(self, name_tabl):
    # Виведення оновленої бази даних (замініть print на необхідні дії)
        updated_colors = name_tabl.query.order_by(name_tabl.color).all()
        print(f"ДИВИМОСЬ БАЗУ {updated_colors}")
        for color in updated_colors:
            print(f'Number: {color.color, color.quantity}')
        db.session.close()
        return updated_colors

    def count_flag(self, text):
        if "#взял" in text:
            return "#взял"
        if "#склад" in text:
            return "#склад"
        if "#редактируєм" in text:
            return "#склад"

    def count_size(self, text):
        if "45:" in text:
            return Colorrep45, "45:"
        if "35:" in text:
            return Colorrep35, "35:"

    def responce_text(self, data, size):
        text = f"{size}\n"
        for item in data:
            text += f"{item.color}х{item.quantity}, "
        return text

    def actual_count(self):
        updated_35 = Colorrep35.query.order_by(Colorrep35.color).all()
        updated_45 = Colorrep45.query.order_by(Colorrep45.color).all()
        count1 = self.count_all(updated_35)
        count2 = self.count_all(updated_45)
        text = f"35:\n"
        for item in updated_35:
            text += f"{item.color}х{item.quantity}, "
        text += f"\nКількість в 35: {count1} \n"
        text += f"\n45:\n"
        for item in updated_45:
            text += f"{item.color}х{item.quantity}, "
        text += f"\nКількість в 45: {count2} \n"
        sum_count = count1 + count2
        text += f"\nЗагальна кількість: {sum_count}"
        db.session.close()
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

    def manager_bot(self, text):
        if "#взял" in text or "#склад" in text:
            if "35:" in text or "45:" in text:
                print("ПРАЦЮЄ")
                data = self.parse_text(text)
                flag = self.count_flag(text)
                if "35:" in text and "45:" in text:
                    clean_35, clean_45 = self.crete_two(text)
                    self.update_base(clean_35, Colorrep35, flag)
                    self.update_base(clean_45, Colorrep45, flag)
                else:
                    print(data)
                    base, size = self.count_size(text)
                    self.update_base(data, base, flag)
                    print(f"ОСЬ ВИЙШЛО {data, flag, size}")
                create_response = self.actual_count()
                return create_response


