import json, re

file_areas = "nova_poshta/create_data/areas_dov/areas_ua.json"

def json_read_dict(file):
    with open(file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
def json_read_dict2(file, description):
    with open(file, "w", encoding="utf-8") as file:
        json.dump(description, file, indent=4, ensure_ascii=False)

def getAreas(AreaName):
    read_file = json_read_dict(file_areas)
    resp=None
    for item in read_file["data"]:
        if AreaName in item["Description"]:
            resp = item["Ref"]
            print(f"Знайшли украинську {resp}")
        if AreaName in item["DescriptionRu"]:
            resp = item["Ref"]
            print(f"Знайшли російску {resp}")
    return resp

def getAreasName(AreaName):
    read_file = json_read_dict(file_areas)
    resp=None
    for item in read_file["data"]:
        if AreaName in item["Description"]:
            resp = item
            print(f"Знайшли украинську {resp}")
            break
        if AreaName in item["DescriptionRu"]:
            resp = item
            print(f"Знайшли російску {resp}")
            break
    return resp

def addDiscription():
    read_temp = json_read_dict("dovidka/tempArea.json")
    read_ua = json_read_dict(file_areas)

    for item, itemData in zip(read_ua["data"], read_temp["data"]):
            item["Ref"] = itemData["Ref"]
    json_read_dict2(file_areas, read_ua)





