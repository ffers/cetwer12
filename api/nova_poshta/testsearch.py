from .create_data import get_search_warhouse
import os, json

bufer = {"CityName":"", "CityRef":"", "TypeOfWarehouseRef":"", "WarehouseId":"", "FindByString":"" }

directory_to_search = "nova_poshta/create_data/dov_test/"
directory_to_save = "nova_poshta/create_data/warehouses/"
directory_to_save_dh = "nova_poshta/create_data/warehouses_dh/"
structured_data = {"City": []}
city_war_dont_have = {"City": []}
warehouse_data = {}
file_count = 1
file_count_dh = 1

def addWarehouse(warehouse):
    warehouse_info = {"Description": warehouse["Description"], "DescriptionRu": warehouse["DescriptionRu"],
                      "ShortAddress": warehouse["ShortAddress"], "ShortAddressRu": warehouse["ShortAddressRu"],
                      "TypeOfWarehouse": warehouse["TypeOfWarehouse"], "Ref": warehouse["Ref"]}
    return warehouse_info


def saveWarehouse(resp, load_city_ref):
    if resp["data"]:
        print(resp["data"][0]["ShortAddress"])
        # Город не найден, добавляем новый
        # Description
        # DescriptionRu
        # ShortAddress
        # ShortAddressRu
        # CityRef
        # CityDescription
        # CityDescriptionRu
        # SettlementRef
        # Ref
        # Number
        # SettlementDescription
        # SettlementAreaDescription
        # SettlementRegionsDescription
        department = resp["data"][0]
        city_info = {"City": department["SettlementDescription"],"CityDescription": department["CityDescription"], "Region": department["SettlementRegionsDescription"],
                     "Area": department["SettlementAreaDescription"], "CityRef": department["CityRef"], "Warehouse":[], "Post":[]}
        page = 1
        while True:
            for warehouse in resp["data"]: # проходимо по всім відділенням міста
                warehouse_info = addWarehouse(warehouse)
                post = "f9316480-5f2d-425d-bc2c-ac7cd29decf0"
                if post in warehouse["TypeOfWarehouse"]:
                    city_info["Post"].append(warehouse_info)
                if post not in warehouse["TypeOfWarehouse"]:
                    city_info["Warehouse"].append(warehouse_info)
            page += 1
            resp = requestsRef(resp["data"][0]["CityRef"], page)
            if not resp["data"]:
                # Выход из цикла відділень, если нет данных
                break
        structured_data["City"].append(city_info)
        department_size = len(json.dumps(structured_data, ensure_ascii=False, indent=2))
        chunk_size_limit = 1 * 1024   # 10 МБ в байтах
        current_chunk_size = 0
        global file_count
        if current_chunk_size + department_size > chunk_size_limit:

            file_count += 1
            with open(f'{directory_to_save}data_chunk_{file_count}.json', 'w') as file:
                json.dump(structured_data, file, ensure_ascii=False, indent=2)

            current_chunk_size = 0
            current_chunk_size += department_size
            print(current_chunk_size)
            structured_data["City"] = []

        if structured_data["City"]:
            print(f"запис структури {structured_data}")
            with open(f'{directory_to_save}data_chunk_{file_count}.json', 'w') as file:
                json.dump(structured_data, file, ensure_ascii=False, indent=2)
    else:
        city_info = {"CityRef": load_city_ref["Ref"]}

        city_war_dont_have["City"].append(city_info)
        city_war_dont_have_size = len(json.dumps(city_war_dont_have, ensure_ascii=False, indent=2))
        chunk_size_limit = 1 * 1024 * 1024  # 10 МБ в байтах
        current_chunk_size2 = 0
        global file_count_dh
        if current_chunk_size2 + city_war_dont_have_size > chunk_size_limit:
            file_count_dh += 1
            with open(f'{directory_to_save_dh}data_dh_{file_count_dh}.json', 'w') as file:
                json.dump(city_war_dont_have, file, ensure_ascii=False, indent=2)

            current_chunk_size2 = 0
            current_chunk_size2 += city_war_dont_have_size
            print(current_chunk_size2)
            city_war_dont_have["City"] = []

        if city_war_dont_have["City"]:
            print(f"запис city_war_dont_have {city_war_dont_have}")
            with open(f'{directory_to_save_dh}data_dh_{file_count_dh}.json', 'w') as file:
                json.dump(city_war_dont_have, file, ensure_ascii=False, indent=2)

def openDirectory(directory):
    files = os.listdir(directory) # откриваем папку
    files.sort()
    for filename in files: # перебираем файли
        print(filename)
        filepath = search_data_in_files(directory, filename) # первий файл
        if filepath: # если найден // но мені потрібно перед передачею файлу до перебору
                    # міст перевірити у всіх файлах чи нема цього міста тому добавлю сбор всіх данних в json
            json_data = openFile(filepath)
            return json_data


def requestsRef(city_ref, page):
    bufer.update({"CityRef": city_ref, "Page": page})
    resp = get_search_warhouse(bufer)
    return resp

def openFile(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def search_data_in_files(directory, filename): # Проходим по всем файлам в каталоге
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath) and filename.endswith('.json'):
        return filepath
    else:
        return None

def definSaveData(): # проверяєм данние уже обработание
    loadData = openDirectory(directory_to_search)
    saveData = openDirectory(directory_to_save)
    save_war_dh = openDirectory(directory_to_save_dh)
    if saveData:
        global structured_data
        structured_data = saveData
    if save_war_dh:
        global city_war_dont_have
        city_war_dont_have = save_war_dh



def page_for(city_info, page):
    city_data, city_data_dh = None, None

    saveData = openDirectory(directory_to_save)
    save_war_dh = openDirectory(directory_to_save_dh)
    if saveData:
        for city_data in saveData:

            print(f"saveData {saveData}")
            city_data = next((city for city in saveData["City"] if city.get("CityRef") == city_info), None)
            print(f"city_data {city_data}")
            break
    if save_war_dh:
        for city_data_dh in save_war_dh:

            city_data_dh = next((city for city in save_war_dh["City"] if city.get("CityRef") == city_info), None)
            print(f"city_data_dh {city_data_dh}")
            break
    if not city_data and not city_data_dh:
        print(f"city_info {city_info}")
        resp = requestsRef(city_info, page)
        return resp

def openDirectoryCity(directory):
    files = os.listdir(directory)  # откриваєм папку словарей городов
    files.sort()
    return files

def throughFiles(filename, directory):
    print(filename)
    filepath = search_data_in_files(directory, filename)
    if filepath:
        # try:
        json_data = openFile(filepath)  # если все ок получаем json словарей городов
        return json_data

def iteretionCity(city_info):
    page = 1
    resp = page_for(city_info.get('Ref'),
                    page)  # проверяєм если в збережиних данних місто та робимо запрос // хоча можна було перевірити у вже існуючому словарі sctured а не відкривати файл
    return resp

def task_control(directory):
    files = openDirectoryCity(directory)
    for filename in files: # проходим по файлам
        json_data = throughFiles(filename, directory)
        definSaveData()  # проверяєм данние уже обработание и добавляєм в словарь
        for city_info in json_data["data"]:  # переберираем каждий город
            resp = iteretionCity(city_info)
            saveWarehouse(resp, city_info)  # якщо є відповідь сервера зберігаємо її

            # except Exception as e:
            #     print(f'Ошибка при обработке файла {filename}: {e}')
        # else:
        #     print("файл не відчинився")
        #     break


def maim():
    task_control(directory_to_search)



