from .create_data import get_search_warhouse
import os, json, copy

class SearchForDB:
    def __init__(self):
        pass

    def search_data_in_files(self, directory, filename): # Проходим по всем файлам в каталоге
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filename.endswith('.json'):
            return filepath
        else:
            return None
    
    def openFile(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data

    def openCityToSearch(self):
        dataSave = {"City": []}
        directory = "nova_poshta/create_data/dovidka/"
        files = os.listdir(directory) # откриваем папку
        files.sort()
        for filename in files: # перебираем файли
            filepath = self.search_data_in_files(directory, filename) # первий файл
            if filepath: # если найден // но мені потрібно перед передачею файлу до перебору
                        # міст перевірити у всіх файлах чи нема цього міста тому добавлю сбор всіх данних в json
                json_data = self.openFile(filepath)
                # print(f"дивимось json_dada: {json_data}")
                dataSave["City"].extend(json_data["data"])
        return dataSave

    def task_control(self):
        city_to_search = self.openCityToSearch() # отримуємо список міст для пошуку 
        for city_info in city_to_search["City"]:
            # перевіряємо чи є місто в списку з відділеннями
            city_data = next((city for city in structured_data["City"] if city.get("CityRef") == city_info["Ref"]), None) 
            # перевіряємо чи є місто в списку без відділень 
            city_data_dh = next((city for city in city_war_dont_have["City"] if city.get("CityRef") == city_info["Ref"]), None)
            print(city_info["Description"])
            if city_data or city_data_dh:
                pass # можно перевірити по статусу WarehouseStatus та перевірити чи є це відділеня в наявності
                # також я думаю зо можна завантажити усі поштомати або відідлення по місту та перевірити чи всі з них є у мене
            if not city_data and not city_data_dh: # не найшли реф починає роботу
                resp = iteretionCity(city_info) # працює page_for, це запуск реквест з ref
                # print(f"відповідь {resp}")
                saveWarehouse(resp, city_info)
        print("Роботу завершенно!")


