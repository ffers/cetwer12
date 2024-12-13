from .create_data import get_search_warhouse
import os, json, copy

bufer = {"CityName":"", "CityRef":"", "TypeOfWarehouseRef":"", "WarehouseId":"", "FindByString":"" }

directory_to_search = "api/nova_poshta/create_data/dovidka/"
directory_to_save = "api/nova_poshta/create_data/warehouses/"
directory_to_save_dh = "api/nova_poshta/create_data/warehouses_dh/"
city_to_search = {}
structured_data = {"City": []}
city_war_dont_have = {"City": []}
cache_war = {"City": []}
cache_war_dh = {"City": []}
warehouse_data = {}
file_count = 0
file_count_dh = 0

def addWarehouse(warehouse):
    warehouse_info = {"Description": warehouse["Description"], "DescriptionRu": warehouse["DescriptionRu"],
                      "ShortAddress": warehouse["ShortAddress"], "ShortAddressRu": warehouse["ShortAddressRu"],
                      "TypeOfWarehouse": warehouse["TypeOfWarehouse"], "Ref": warehouse["Ref"]}
    return warehouse_info


def saveWarehouse(load_city, load_city_ref):
    if load_city["data"]:
        department = load_city["data"][0]
        city_info = {"City": department["SettlementDescription"], "CityDescription": department["CityDescription"],
                     "Region": department["SettlementRegionsDescription"],
                     "Area": department["SettlementAreaDescription"], "CityRef": department["CityRef"], "Warehouse": [],
                     "Post": []}
        page = 1
        while True:
            for warehouse in load_city["data"]: # проходимо по всім відділенням міста
                warehouse_info = addWarehouse(warehouse)
                post = "f9316480-5f2d-425d-bc2c-ac7cd29decf0"
                if post in warehouse["TypeOfWarehouse"]:
                    city_info["Post"].append(warehouse_info)
                if post not in warehouse["TypeOfWarehouse"]:
                    city_info["Warehouse"].append(warehouse_info)
            page += 1
            load_city = requestsRef(load_city["data"][0]["CityRef"], page)
            if not load_city["data"]:
                # Выход из цикла відділень, если нет данных
                break
        cache_war["City"].append(city_info)
        structured_data["City"].append(city_info)
        department_size = len(json.dumps(cache_war, ensure_ascii=False, indent=2))
        chunk_size_limit = 10 * 1024 * 1024  # 10 МБ в байтах
        current_chunk_size = 0
        global file_count
        if current_chunk_size + department_size > chunk_size_limit:
            cache_war["City"] = []
            cache_war["City"].append(city_info)

            print(f"filecount save: {file_count}")
            print(f"запис кешвар в новий файл {cache_war}")
            file_count += 1
            current_chunk_size = 0
            current_chunk_size += department_size
            print(current_chunk_size)

        if cache_war["City"]:
            with open(f'{directory_to_save}data_chunk_{file_count}.json', 'w') as file:
                json.dump(cache_war, file, ensure_ascii=False, indent=2)
    else:
        city_info = {"CityRef": load_city_ref["Ref"]}

        cache_war_dh["City"].append(city_info)
        city_war_dont_have["City"].append(city_info)
        city_war_dont_have_size = len(json.dumps(cache_war_dh, ensure_ascii=False, indent=2))
        chunk_size_limit = 10 * 1024 * 1024  # 10 МБ в байтах
        current_chunk_size2 = 0
        global file_count_dh
        if current_chunk_size2 + city_war_dont_have_size > chunk_size_limit:
            cache_war_dh["City"] = []
            cache_war_dh["City"].append(city_info)
            file_count_dh += 1
            with open(f'{directory_to_save_dh}data_dh_{file_count_dh}.json', 'w') as file:
                json.dump(cache_war_dh, file, ensure_ascii=False, indent=2)

            current_chunk_size2 = 0
            current_chunk_size2 += city_war_dont_have_size
            print(f"розмір file_dh {current_chunk_size2}")


        if cache_war_dh["City"]:
            with open(f'{directory_to_save_dh}data_dh_{file_count_dh}.json', 'w') as file:
                json.dump(cache_war_dh, file, ensure_ascii=False, indent=2)

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

def openDirectory(directory, flag):
    dataSave = {"City": []}
    files = os.listdir(directory) # откриваем папку
    files.sort()
    for filename in files: # перебираем файли
        # print(filename)
        filepath = search_data_in_files(directory, filename) # первий файл
        if filepath: # если найден // но мені потрібно перед передачею файлу до перебору
                    # міст перевірити у всіх файлах чи нема цього міста тому добавлю сбор всіх данних в json
            json_data = openFile(filepath)
            # print(f"дивимось json_dada: {json_data}")
            if flag == "loaddata":
                dataSave["City"].extend(json_data["data"])
            if flag == "savedata":
                global file_count
                file_count += 1
                print(f"file count: {file_count}")
                dataSave["City"].extend(json_data["City"])
            if flag == "save_war_dh":
                global file_count_dh
                file_count_dh += 1
                print(f"file count dh: {file_count_dh}")
                dataSave["City"].extend(json_data["City"])

        # print(f"дивимось кінцевий dataSave {dataSave}")
    return dataSave

def definSaveData(): # проверяєм данние уже обработание
    loadData = openDirectory(directory_to_search, "loaddata")
    saveData = openDirectory(directory_to_save, "savedata")
    save_war_dh = openDirectory(directory_to_save_dh, "save_war_dh")
    global file_count
    global file_count_dh
    if loadData:
        print(f"інфа для пошуку {loadData}")
        global city_to_search
        city_to_search = copy.deepcopy(loadData)
    if saveData["City"]:
        global structured_data, cache_war
        structured_data = copy.deepcopy(saveData)
        print(f"начальная дата структур {structured_data}")
        cache_war = copy.deepcopy(saveData)
    else:
        file_count = 1
        print(f"file count {file_count}")
    if save_war_dh["City"]:
        print(f"все що збережено без відділень {save_war_dh}")
        global city_war_dont_have, cache_war_dh
        city_war_dont_have = copy.deepcopy(save_war_dh)
        cache_war_dh = copy.deepcopy(save_war_dh)
    else:
        file_count_dh = 1

def page_for(city_info, page):
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

def task_control():
    definSaveData()
    for city_info in city_to_search["City"]:
        city_data = next((city for city in structured_data["City"] if city.get("CityRef") == city_info["Ref"]), None)
        city_data_dh = next((city for city in city_war_dont_have["City"] if city.get("CityRef") == city_info["Ref"]), None)
        print(city_info["Description"])
        if not city_data and not city_data_dh: # не найшли реф починає роботу
            resp = iteretionCity(city_info) # працює page_for, це запуск реквест з ref
            # print(f"відповідь {resp}")
            saveWarehouse(resp, city_info)
    print("Роботу завершенно!")



def maim():
    task_control()



