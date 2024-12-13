from .create_data import get_search_warhouse
import os, json, copy, hashlib

bufer = {"CityName":"", "CityRef":"", "TypeOfWarehouseRef":"", "WarehouseId":"", "FindByString":"" }

directory_to_search = "api/nova_poshta/create_data/dovidka/"
directory_to_save = "api/nova_poshta/create_data/warehouses_buc/"
directory_to_save_dh = "api/nova_poshta/create_data/warehouses_dh/"
dir_warehouse_uniq = "api/nova_poshta/create_data/warehouses_uniq/"
city_to_search = {}
structured_data = {"City": []}
uniq_city = {"City": []}
city_war_dont_have = {"City": []}
cache_war = {"City": []}
cache_war_dh = {"City": []}
warehouse_data = {}
file_count = 0
file_count_dh = 0
flag_add_post = "addPost"
file_count_citys = 0

def addWarehouse(warehouse):
    warehouse_info = {"Description": warehouse["Description"], "DescriptionRu": warehouse["DescriptionRu"],
                      "ShortAddress": warehouse["ShortAddress"], "ShortAddressRu": warehouse["ShortAddressRu"],
                      "TypeOfWarehouse": warehouse["TypeOfWarehouse"], "Ref": warehouse["Ref"], "StatusChange": "Edit" }
    return warehouse_info


def saveWarehouse(load_city, load_city_ref):
    global file_count_citys
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
        file_with_citys = openDirectory(directory_to_save, flag_add_post, load_city_ref["CityRef"])
        for city in file_with_citys["City"]:
            if city["CityRef"] == load_city_ref["CityRef"]:
                city.update(city_info)
                break
        # cache_war["City"].append(city_info)
        for city in uniq_city["City"]:
            if city["CityRef"] == load_city_ref["CityRef"]:
                city.update(city_info)
                break

        # department_size = len(json.dumps(file_with_citys, ensure_ascii=False, indent=2))
        # chunk_size_limit = 10 * 1024 * 1024  # 10 МБ в байтах
        # current_chunk_size = 0
        # global file_count_citys
        # if current_chunk_size + department_size > chunk_size_limit:
        #     file_with_citys["City"] = []
        #     file_with_citys["City"].append(city_info)
        #
        #     print(f"filecount save: {file_count}")
        #     print(f"запис кешвар в новий файл {cache_war}")
        #     file_count_citys += 1
        #     current_chunk_size = 0
        #     current_chunk_size += department_size
        #     print(current_chunk_size)

        if file_with_citys["City"]:
            with open(f'{directory_to_save}data_chunk_{file_count_citys}.json', 'w') as file:
                json.dump(file_with_citys, file, ensure_ascii=False, indent=2)

            file_count_citys = 0
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

def openDirectory(directory, flag, searchRef=None):
    dataSave = {"City": []}
    files = os.listdir(directory) # откриваем папку
    files.sort()
    for filename in files: # перебираем файли
        # print(filename)
        filepath = search_data_in_files(directory, filename) # первий файл
        if filepath:
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
            if flag == "addPost":
                global file_count_citys
                file_count_citys += 1
                for city in json_data["City"]:
                    if searchRef == city["CityRef"]:
                        dataSave["City"].extend(json_data["City"])
                        break

        # print(f"дивимось кінцевий dataSave {dataSave}")
    return dataSave

def definSaveData(): # проверяєм данние уже обработание
    loadData = openDirectory(directory_to_search, "loaddata")
    saveData = openDirectory(directory_to_save, "savedata")
    save_war_dh = openDirectory(directory_to_save_dh, "save_war_dh")
    global file_count
    global file_count_dh
    if loadData:
        # print(f"інфа для пошуку {loadData}")
        global city_to_search
        city_to_search = copy.deepcopy(loadData)
    if saveData["City"]:
        global structured_data, cache_war
        structured_data = copy.deepcopy(saveData)
        # print(f"начальная дата структур {structured_data}")
        cache_war = copy.deepcopy(saveData)
    else:
        file_count = 1
        print(f"file count {file_count}")
    if save_war_dh["City"]:
        # print(f"все що збережено без відділень {save_war_dh}")
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

def iteretionCity2(city_info):
    page = 2
    resp = page_for(city_info.get('Ref'),
                    page)  # проверяєм если в збережиних данних місто та робимо запрос // хоча можна було перевірити у вже існуючому словарі sctured а не відкривати файл
    return resp

def write_file(unique_city):
    cache_uniq_city = {"City": []}
    global file_count_citys_uniq
    file_count_citys_uniq = 1
    for city in unique_city:
        print("!!!! працюєм з унікальними данними")
        cache_uniq_city["City"].append(city)
        department_size = len(json.dumps(cache_uniq_city, ensure_ascii=False, indent=2))
        chunk_size_limit = 10 * 1024 * 1024  # 10 МБ в байтах
        current_chunk_size = 0
        if current_chunk_size + department_size > chunk_size_limit:
            with open(f'{dir_warehouse_uniq}data_chunk_{file_count_citys_uniq}.json', 'w') as file:
                json.dump(cache_uniq_city, file, ensure_ascii=False, indent=2)
            cache_uniq_city["City"] = []
            cache_uniq_city["City"].append(city)
            print(f"filecount save: {file_count}")
            print(f"запис кешвар в новий файл {cache_war}")
            file_count_citys_uniq += 1
            current_chunk_size = 0
            current_chunk_size += department_size
            print(current_chunk_size)


def hash_dict_sha256(data):
    json_str = json.dumps(data, sort_keys=True)
    hash_sha256 = hashlib.sha256(json_str.encode()).hexdigest()
    return hash_sha256

def find_dublicate(citys):
    seen = set()
    unique_city = {"City": []}
    for index, city in enumerate(citys["City"]):
        city_hash = hash_dict_sha256(city)
        if city_hash not in seen:
            unique_city["City"].append(city)
            seen.add(city_hash)
        else:
            print(f"Знайдено дублікат номер {index}")
    write_file(unique_city)
    return unique_city

def task_control():
    definSaveData()
    global uniq_city
    print(structured_data)
    uniq_city = find_dublicate(structured_data)
    print(uniq_city, "uniq_city")
    for city_info in uniq_city["City"]:
        city_name = city_info["City"]
        print(f"!!!! Опрацюваєм місто {city_name}")
        if "StatusChange" not in city_info:
            page2 = iteretionCity2(city_info)
            # print(page2)
            # city_data = next((city for city in structured_data["City"] if city.get("CityRef") == city_info["Ref"]), None)
            # найшли данні починаєм роботу
            saveWarehouse(page2, city_info)
    print("Роботу завершенно!")



def maim():
    task_control()



