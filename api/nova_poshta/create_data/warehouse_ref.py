import json, logging, re, copy
from . import searchSettlements, getAreasName, get_search_warhouse, NpClient


NP = NpClient()
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

class WarehouseRefCl():
    def __init__(self, sun=None):
        self.SUN = sun

    def searchRegions(self, AreaRef):
        getRegion = NP.getSettlementCountryRegion(AreaRef)
        return getRegion
    def WarehouseFilter(self, address):
        Warehouse = ""
        TypeOfWarehouseRef = None
        self.SUN.update({"OptionsSeat": None})
        if "Поштомат №" in address:
            print("Знайдено Поштомат")
            Warehouse = re.search(r'Поштомат №\s*(\d+)', address)
            Warehouse = Warehouse.group(1).strip()
            TypeOfWarehouseRef = "f9316480-5f2d-425d-bc2c-ac7cd29decf0"
            self.SUN.update(OptionsSeat)
        elif "Почтомат №" in address:
            print("Знайдено Поштомат")
            Warehouse = re.search(r'Почтомат №\s*(\d+)', address)
            Warehouse = Warehouse.group(1).strip()
            TypeOfWarehouseRef = "f9316480-5f2d-425d-bc2c-ac7cd29decf0"
            self.SUN.update(OptionsSeat)
        elif "до 30 кг" in address or "до 10 кг" in address or "до 5 кг" in address:
            TypeOfWarehouseRef = "841339c7-591a-42e2-8233-7a0a00f0ed6f"
            if "№" in address:
                print("Знайдено відділеня до 30 або до 10 кг")
                Warehouse = re.search(r'№\s*(\d+)', address)
                Warehouse = Warehouse.group(1).strip()
            if "Пункт" in address:
                print("Знайдено Пункт видачи.")
                self.SUN.update({"warehouse_n": "Пункт видачі"})
        elif ("№" in address and "Поштомат" not in address
              and "Почтомат" not in address and "до 30 кг" not in address
              and "до 10 кг" not in address and "до 5 кг" not in address):
            print("Знайдено Відділення")
            Warehouse = re.search(r'№\s*(\d+)', address)
            Warehouse = Warehouse.group(1).strip()
            TypeOfWarehouseRef = "9a68df70-0267-42a8-bb5c-37f427e36ee4"
        else:
            print("Відділення або Поштомат не знайдені")
            print(Warehouse)
        self.SUN.update({"warehouse_n": Warehouse, "TypeOfWarehouseRef": TypeOfWarehouseRef})
        return Warehouse, TypeOfWarehouseRef

    def CityFilter(self, order):
        words = re.search(r'[A-ZА-ЯІЄЇ][^,(]+(?=\()*', order)
        CityName = None
        if words:
            CityName = words[0].strip()
            print(CityName)
        return CityName
    def extract_area(self, address):
        word = None
        if "обл" in address:
            words = re.findall(r"([А-ЯІЇЄҐ][^\(\),\s]*?)\.*\s*обл", address) # на всяк випадок старе [?<=\(]([А-ЯA-ZА-ЯІЄЇ]\D+)(?=\sобл)
            print(words)
            if len(words) != 0:
                word = words[0]
                print(word)
        return word

    def extract_region(self, address):
        word = None
        if re.findall(r"[?<=\(]([А-ЯA-ZА-ЯІЄЇ]\D+)(?=\sр-н)", address):
            words = re.findall(r"[?<=\(.,*][А-ЯA-ZА-ЯІЄЇ]*[\D+]*([А-ЯA-ZА-ЯІЄЇ]\D+)(?=\sр-н)", address)
            if len(words) != 0:
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
                    print("Значення вулиці не знайдені")

        print(desc_address)

        return desc_address

    def search_area(self, area, data_list):
        area_data = getAreasName(area)  # шукаєм в довідці своїй
        print(area_data)
        ref = None
        if area_data:
            print(area_data)
            area_ua = area_data["Description"]
            print("Є область")
            for item_seached_data in data_list:
                item_area = item_seached_data["Area"]
                if area_ua in item_seached_data["Area"]:
                    ref = item_seached_data["DeliveryCity"]
                    print(f"Найденая область {item_area} совпадает с найденой в заказе {area_ua}")
                    break
                else:
                    print(f"Найденая область {item_area} не совпадает c найденой в заказе {area_ua}")
        else:
            print("Області нема")
        print(ref)
        return ref

    def search_region(self, region, data_list):
        print(region)
        ref = None
        if region:
            print(region)
            print("Є р-н")
            for item_seached_data in data_list:
                item_region = item_seached_data["Region"]
                if region in item_seached_data["Region"]:
                    ref = item_seached_data["DeliveryCity"]
                    print(f"Найдений р-н {item_region} совпадает с найденим в заказе {region}")
                    break
                else:
                    print(f"Найдений р-н  {item_region} не совпадает c найденим в заказе {region}")
        else:
            print("Р-ну нема")
        print(ref)
        return ref

    def extract_city_ref(self, city, area=None, region=None):
        ref = None
        data_city_where_searched = searchSettlements(city)
        data_list = data_city_where_searched["data"][0]["Addresses"]
        print(city)
        print(data_list)
        ref = data_list[0]["DeliveryCity"]
        if area:
            ref = self.search_area(area, data_list)
        if region:
            ref = self.search_region(region, data_list)
            if not ref:
                ref = self.search_area(area, data_list)
        return ref

    def search_address(self, order):
        warh_ref = order["delivery_provider_data"]["recipient_warehouse_id"]
        resp = NP.get_s_war_ref(warh_ref)
        print(f"інфа по реф {resp}")
        return resp

    def compact_data(self, order):
        data_dict = {}
        data_dict.clear()
        order_address = order["delivery_address"]
        FindByString = self.extract_desc_street(order_address)
        Region = self.extract_region(order_address)
        Area = self.extract_area(order_address)
        data_address = self.search_address(order)
        CityName = data_address["data"][0]["CityDescription"]
        self.SUN.update({"CityName": CityName})
        Warehouse, TypeOfWarehouseRef = self.WarehouseFilter(order_address)
        HouseNumber = None
        CityRef = data_address["data"][0]["CityRef"]
        data_dict = {
            "CityName": CityName,
            "WarehouseId": Warehouse,
            "FindByString": FindByString,
            "Region": Region,
            "Area": Area,
            "TypeOfWarehouseRef": TypeOfWarehouseRef,
            "HouseNumber": HouseNumber,
            "CityRef" : CityRef,
            "CityRecipient": CityRef,
            "Page": 1
        }
        print(data_dict)
        return data_dict

    def warehouse_city_warh(self, data_dict_g): # шукаєм по місту та відділенню потім треба звірити область якщо є, р-н якщо є, та вулицю по одній із мов
        resp = None
        FindByString = ""
        TypeOfWarehouseRef = ""
        data_dict = copy.deepcopy(data_dict_g)
        data_dict.update({"FindByString": FindByString, "TypeOfWarehouseRef": TypeOfWarehouseRef})
        print(f"Після оновленя {data_dict}")
        data_np = get_search_warhouse(data_dict)
        print(data_np)
        if data_np["info"]["totalCount"] != 0:
            resp = data_np
        return resp

    def warehouse_city(self, data_dict): # шукаєм по місту та відділенню потім треба звірити область якщо є, р-н якщо є, та вулицю по одній із мов
        resp = None
        data_np = get_search_warhouse(data_dict)
        print(data_np)
        if data_np["info"]["totalCount"] != 0:
            resp = data_np
        return resp

    def warehouse_str(self, data_dict_g):
        resp = None
        data_dict = copy.deepcopy(data_dict_g)
        print(f"Пошук по місту {data_dict}")
        CityName = ""
        data_dict.update({"CityName": CityName})
        print(f"Після оновленя {data_dict}")
        data_np = get_search_warhouse(data_dict)
        print(data_np)
        if data_np["info"]["totalCount"] != 0:
            resp = data_np
        return resp

    def warehouse_area(self, data_dict_g):
        data_dict = copy.deepcopy(data_dict_g)
        resp = None
        print(data_dict)
        CityName = ""
        Region = ""
        data_dict.update({"CityName": CityName, "Region": Region})
        print("После обновление CityName")
        print(data_dict)
        data_np = get_search_warhouse(data_dict)
        print(data_np)
        if data_np["info"]["totalCount"] != 0:
            resp = data_np
        return resp

    def RefWarehouse(self, order):
        ref = None
        data_warehouse = None
        data_dict_g = self.compact_data(order)
        print(f"Data_dict > {data_dict_g}")
        self.SUN.update(data_dict_g)
        return {'ok':True}
        # search_for_city = self.warehouse_city(data_dict_g)
        # if search_for_city != None:
        #     print(f"По всім доступним данним найшли ref: {search_for_city}, не точний вариант")
        #     data_warehouse = search_for_city
        # if data_warehouse == None:
        #     search_for_city_warh = self.warehouse_city_warh(data_dict_g)
        #     if search_for_city_warh != None:
        #         print(f"По місту та номеру відділення найшли ref: {search_for_city_warh}, не точний вариант")
        #         data_warehouse = search_for_city_warh
        # if data_warehouse == None:
        #     search_for_str = self.warehouse_str(data_dict_g)
        #     if search_for_str != None:
        #         data_warehouse = search_for_str
        #         print(f"За виключенням міста найшли ref: {search_for_str}, більш точний вариант")
        # if data_warehouse == None:
        #     search_for_area = self.warehouse_area(data_dict_g)
        #     if search_for_area != None:
        #         data_warehouse = search_for_area
        #         print(f"За виключенням міста та району найшли ref: {search_for_area},  вариант 4")
        #     else:
        #         print("Неспрацював не один з варіантів!!!")





#
