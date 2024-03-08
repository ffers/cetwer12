from create_data.request_dov import getAreasName

data = {'success': True, 'data': [{'TotalCount': 38, 'Addresses': [
    {'Present': 'с. Катеринівка, Кіровоградський р-н, Кіровоградська обл.', 'Warehouses': 3,
     'MainDescription': 'Катеринівка', 'Area': 'Кіровоградська', 'Region': 'Кіровоградський',
     'SettlementTypeCode': 'с.', 'Ref': '0e5fce51-4b3a-11e4-ab6d-005056801329',
     'DeliveryCity': '59227c6d-29c2-11eb-80fb-b8830365bd04', 'AddressDeliveryAllowed': True,
     'StreetsAvailability': False, 'ParentRegionTypes': 'область', 'ParentRegionCode': 'обл.', 'RegionTypes': 'район',
     'RegionTypesCode': 'р-н'}, {'Present': 'с. Катеринівка, Веселинівський р-н, Миколаївська обл.', 'Warehouses': 2,
                                 'MainDescription': 'Катеринівка', 'Area': 'Миколаївська', 'Region': 'Веселинівський',
                                 'SettlementTypeCode': 'с.', 'Ref': '0d9ef0be-4b3a-11e4-ab6d-005056801329',
                                 'DeliveryCity': 'bb95cd4a-e687-11e9-b48a-005056b24375', 'AddressDeliveryAllowed': True,
                                 'StreetsAvailability': False, 'ParentRegionTypes': 'область',
                                 'ParentRegionCode': 'обл.', 'RegionTypes': 'район', 'RegionTypesCode': 'р-н'},
    {'Present': 'с. Катеринівка, Лозівський р-н, Харківська обл.', 'Warehouses': 2, 'MainDescription': 'Катеринівка',
     'Area': 'Харківська', 'Region': 'Лозівський', 'SettlementTypeCode': 'с.',
     'Ref': '0e83025a-4b3a-11e4-ab6d-005056801329', 'DeliveryCity': 'e1426f3c-3e4c-11eb-80fb-b8830365bd04',
     'AddressDeliveryAllowed': True, 'StreetsAvailability': False, 'ParentRegionTypes': 'область',
     'ParentRegionCode': 'обл.', 'RegionTypes': 'район', 'RegionTypesCode': 'р-н'},
    {'Present': 'с. Катеринівка, Васильківський р-н, Дніпропетровська обл.', 'Warehouses': 2,
     'MainDescription': 'Катеринівка', 'Area': 'Дніпропетровська', 'Region': 'Васильківський',
     'SettlementTypeCode': 'с.', 'Ref': '0dba5485-4b3a-11e4-ab6d-005056801329',
     'DeliveryCity': '358842bd-883e-11e9-898c-005056b24375', 'AddressDeliveryAllowed': True,
     'StreetsAvailability': False, 'ParentRegionTypes': 'область', 'ParentRegionCode': 'обл.', 'RegionTypes': 'район',
     'RegionTypesCode': 'р-н'},
    {'Present': "с. Катеринівка, Мар'їнський р-н, Донецька обл.", 'Warehouses': 2, 'MainDescription': 'Катеринівка',
     'Area': 'Донецька', 'Region': "Мар'їнський", 'SettlementTypeCode': 'с.',
     'Ref': '0ec27b28-4b3a-11e4-ab6d-005056801329', 'DeliveryCity': 'd03cca05-cf28-11e9-b0c5-005056b24375',
     'AddressDeliveryAllowed': False, 'StreetsAvailability': False, 'ParentRegionTypes': 'область',
     'ParentRegionCode': 'обл.', 'RegionTypes': 'район', 'RegionTypesCode': 'р-н'},
    {'Present': 'с. Катеринівка, Сахновщинський р-н, Харківська обл.', 'Warehouses': 2,
     'MainDescription': 'Катеринівка', 'Area': 'Харківська', 'Region': 'Сахновщинський', 'SettlementTypeCode': 'с.',
     'Ref': '0e9f546f-4b3a-11e4-ab6d-005056801329', 'DeliveryCity': '7d3175bf-cf4b-11e9-b0c5-005056b24375',
     'AddressDeliveryAllowed': True, 'StreetsAvailability': False, 'ParentRegionTypes': 'область',
     'ParentRegionCode': 'обл.', 'RegionTypes': 'район', 'RegionTypesCode': 'р-н'},
    {'Present': 'с. Катеринівка, Покровський р-н, Дніпропетровська обл.', 'Warehouses': 2,
     'MainDescription': 'Катеринівка', 'Area': 'Дніпропетровська', 'Region': 'Покровський', 'SettlementTypeCode': 'с.',
     'Ref': '0e0de257-4b3a-11e4-ab6d-005056801329', 'DeliveryCity': '09144ccb-e5ef-11e9-b48a-005056b24375',
     'AddressDeliveryAllowed': True, 'StreetsAvailability': False, 'ParentRegionTypes': 'область',
     'ParentRegionCode': 'обл.', 'RegionTypes': 'район', 'RegionTypesCode': 'р-н'},
    {'Present': 'с. Катеринівка, Кременецький р-н, Тернопільська обл.', 'Warehouses': 2,
     'MainDescription': 'Катеринівка', 'Area': 'Тернопільська', 'Region': 'Кременецький', 'SettlementTypeCode': 'с.',
     'Ref': '0d7d61bf-4b3a-11e4-ab6d-005056801329', 'DeliveryCity': '92615ab6-896e-11ea-a970-b8830365ade4',
     'AddressDeliveryAllowed': True, 'StreetsAvailability': False, 'ParentRegionTypes': 'область',
     'ParentRegionCode': 'обл.', 'RegionTypes': 'район', 'RegionTypesCode': 'р-н'},
    {'Present': 'с. Катеринівка, Білопільський р-н, Сумська обл.', 'Warehouses': 0, 'MainDescription': 'Катеринівка',
     'Area': 'Сумська', 'Region': 'Білопільський', 'SettlementTypeCode': 'с.',
     'Ref': '0dbe5f97-4b3a-11e4-ab6d-005056801329', 'DeliveryCity': '956452b3-4748-11dd-9198-001d60451983',
     'AddressDeliveryAllowed': False, 'StreetsAvailability': False, 'ParentRegionTypes': 'область',
     'ParentRegionCode': 'обл.', 'RegionTypes': 'район', 'RegionTypesCode': 'р-н'},
    {'Present': 'с. Катеринівка, Сарненський р-н, Рівненська обл.', 'Warehouses': 0, 'MainDescription': 'Катеринівка',
     'Area': 'Рівненська', 'Region': 'Сарненський', 'SettlementTypeCode': 'с.',
     'Ref': '0e2c0390-4b3a-11e4-ab6d-005056801329', 'DeliveryCity': '43913a90-9e44-11e9-898c-005056b24375',
     'AddressDeliveryAllowed': True, 'StreetsAvailability': False, 'ParentRegionTypes': 'область',
     'ParentRegionCode': 'обл.', 'RegionTypes': 'район', 'RegionTypesCode': 'р-н'}]}], 'errors': [], 'warnings': [],
 'info': [], 'messageCodes': [], 'errorCodes': [], 'warningCodes': [], 'infoCodes': []}


def search_area(area, data):
    data_list = data["data"][0]["Addresses"]
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

def search_region(region, data):
    data_list = data["data"][0]["Addresses"]
    print(region)
    ref = None
    if region:
        print(region)
        print("Є область")
        for item_seached_data in data_list:
            item_region = item_seached_data["Region"]
            if region in item_seached_data["Region"]:
                ref = item_seached_data["DeliveryCity"]
                print(f"Найдений р-н {item_region} совпадает с найденим в заказе {region}")
                break
            else:
                print(f"Найдений р-н  {item_region} не совпадает c найденим в заказе {region}")
    else:
        print("Області нема")
    print(ref)
    return ref

# def search
def compare_ref_area():

    ref_area = search_area("Днепр", data)
    ref_region = search_region("Покровський", data)