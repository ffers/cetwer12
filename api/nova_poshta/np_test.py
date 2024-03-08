import os, json, requests, time, logging, re
from create_data import get_create_contact, get_search_contact, get_generate_doc, searchSettlements
from create_data import get_search_warhouse, get_create_contragent, get_Setlements, getSettlements_Str
from create_data import NpClient
from create_data import getAreas, getAreasName



chat_id = "-421982888"
delivery_np = 13013934
json_data_prom = "scrypt_order/documents/data.json"
json_data_np_dict = "create_data/json_dict/json_data_np_dict.json"
contact_np = "create_data/json_dict/contact_np.json"
OptionsSeat = { "OptionsSeat" : [
                    {
                    "volumetricVolume":"0.2",
                    "volumetricWidth":"10",
                    "volumetricLength":"10",
                    "volumetricHeight":"10",
                    "weight":"0.2"
                    }]}

dict_ttn_prom = {
              "order_id": "",
              "declaration_id": "",
              "delivery_type": "nova_poshta"
            }

dict_status_prom = {
          "ids": [ 0 ],
          "custom_status_id":  137639
        }

logging.info("Шукаєм прийняті замовлення...")
with open("../common/data.json") as file:
    orders = json.load(file)

class AddressRef():
    def searchRegions(self, AreaRef):
        getRegion = NP.getSettlementCountryRegion(AreaRef)
        return getRegion
    def WarehouseFilter(self, address):
        Warehouse = ""
        TypeOfWarehouseRef = None
        sun.update({"OptionsSeat": None})
        if "Поштомат №" in address:
            print("Знайдено Поштомат")
            Warehouse = re.search(r'Поштомат №\s*(\d+)', address)
            Warehouse = Warehouse.group(1).strip()
            TypeOfWarehouseRef = "f9316480-5f2d-425d-bc2c-ac7cd29decf0"
            sun.update(OptionsSeat)
        elif "Почтомат №" in address:
            print("Знайдено Поштомат")
            Warehouse = re.search(r'Почтомат №\s*(\d+)', address)
            Warehouse = Warehouse.group(1).strip()
            TypeOfWarehouseRef = "f9316480-5f2d-425d-bc2c-ac7cd29decf0"
            sun.update(OptionsSeat)
        elif "№" in address and "Поштомат" not in address and "Почтомат" not in address and "до 30 кг" not in address:
            print("Знайдено Відділення")
            Warehouse = re.search(r'№\s*(\d+)', address)
            Warehouse = Warehouse.group(1).strip()
            TypeOfWarehouseRef = "9a68df70-0267-42a8-bb5c-37f427e36ee4"
        elif "до 30 кг" in address:
            TypeOfWarehouseRef = "841339c7-591a-42e2-8233-7a0a00f0ed6f"
            if "№" in address:
                print("Знайдено відділеня до 30 кг")
                Warehouse = re.search(r'№\s*(\d+)', address)
                Warehouse = Warehouse.group(1).strip()
            if "Пункт" in address:
                print("Знайдено Пункт видачи.")
                sun.update({"warehouse_n": "Пункт видачі"})
        else:
            print("Відділення або Поштомат не знайдені")
            print(Warehouse)
        sun.update({"warehouse_n": Warehouse, "TypeOfWarehouseRef": TypeOfWarehouseRef})
        return Warehouse, TypeOfWarehouseRef

    def CityFilter(self, order):
        words = re.search(r'[A-ZА-ЯІЄЇ][^,(]+', order)
        CityName = words[0].strip()
        sun.update({"CityName": CityName})
        return CityName
    def extract_area(self, address):
        word = None
        if "обл" in address:
            words = re.findall(r"[?<=\(]([А-ЯA-ZА-ЯІЄЇ]\D+)(?=\sобл)", address)
            word = words[0]
        return word

    def extract_region(self, address):
        word = None
        if "р-н" in address:
            words = re.findall(r"[?<=\(]([А-ЯA-ZА-ЯІЄЇ]\D+)(?=\sр-н)", address)
            word = words[0]
        return word
    def extract_desc_street(self, address):
        print(address)
        desc_address = None
        if ":" in address:
            words = re.findall(r"[?<=\:](.*)", address)
            desc_address = words[0].strip()
            print(words)
        else:
            match = re.search(r"\..*?\. (.*?)$", address)
            if match:
                desc_address = match[1]
            else:
                match = re.search(r"\,\s*(.*\D+.*\d+)", address)
                if match:
                    desc_address = match.group(1)
                else:
                    print("Значения улици не найдени")

        print(desc_address)

        return desc_address

    def extract_city_ref(self, city, area=None, region=None):
        data_city_where_searched = searchSettlements(city)
        print(city)
        print(data_city_where_searched)
        data_city_where_searched_item = data_city_where_searched["data"][0]["Addresses"]
        if area:
            area_data = getAreasName(area)
            area_ua = area_data["Description"]
            print("Є область")
            for item_seached_data in data_city_where_searched_item:
                item_area = item_seached_data["Area"]
                if area_ua == item_seached_data["Area"]:
                    ref = item_seached_data["DeliveryCity"]
                    print(f"Найденая область {item_area} найденой в заказе {area_ua}")
                    break
                else:

                    print(f"Найденая область {item_area} не совпадает c найденой в заказе {area_ua}")
        else:
            print("Області нема")
            ref = data_city_where_searched["data"][0]["Addresses"][0]["DeliveryCity"]
        return ref



    def compact_data(self, order):
        order_address = order["delivery_address"]
        FindByString = self.extract_desc_street(order_address)
        Region = self.extract_region(order_address)
        Area = self.extract_area(order_address)
        CityName = self.CityFilter(order_address)
        Warehouse, TypeOfWarehouseRef = self.WarehouseFilter(order_address)
        HouseNumber = None
        CityRef = self.extract_city_ref(CityName, Area, Region)
        data_dict = {
            "CityName": CityName,
            "WarehouseId": Warehouse,
            "FindByString": FindByString,
            "Region": Region,
            "Area": Area,
            "TypeOfWarehouseRef": TypeOfWarehouseRef,
            "HouseNumber": HouseNumber,
            "CityRef" : CityRef
        }
        print(data_dict)
        return data_dict


    def warehouse_city(self, order): # шукаєм по місту та відділенню потім треба звірити область якщо є, р-н якщо є, та вулицю по одній із мов
        resp = None
        data_dict = self.compact_data(order)
        data_np = get_search_warhouse(data_dict)
        print(data_np)
        if data_np["info"]["totalCount"] != 0:
            resp = data_np
        return resp

    def warehouse_str(self, order):
        resp = None
        data_dict = self.compact_data(order)
        print(data_dict)
        CityName = ""
        data_dict.update({"CityName": CityName})
        print("После обновление CityName")
        print(data_dict)
        data_np = get_search_warhouse(data_dict)
        print(data_np)
        if data_np["info"]["totalCount"] != 0:
            resp = data_np
        return resp

    def RefWarehouse(self, order):
        data_warehouse = None
        search_for_city = self.warehouse_city(order)
        if search_for_city != None:
            print(f"По первому попавшемуся городу нашли ref: {search_for_city}, не точний вариант")
            data_warehouse = search_for_city
        elif search_for_city == None:
            search_for_str = self.warehouse_str(order)
            if search_for_str != None:
                data_warehouse = search_for_str
                print(f"По другому варианту нашли ref: {search_for_str}, більш точний вариант")
            else:
                print("Неспрацював не один з варіантів!!!")
        else:
            print("Замовленя без заданого параметру або помилка")
        if data_warehouse != None:
            ref = data_warehouse["data"][0]["Ref"]
            CityRecipient = data_warehouse["data"][0]["CityRef"]
            WarehouseIndex = data_warehouse["data"][0]["WarehouseIndex"]
            sun.update({"CityRecipient": CityRecipient, "RecipientWarehouseIndex": WarehouseIndex})
        return ref




