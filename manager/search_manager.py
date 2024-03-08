from api.nova_poshta.create_data import NpClient
from helperkit import FileKit

fl_cl = FileKit()
np_cl = NpClient()

class Search_NP:
    def __init__(self):
        self.file_json = "../api/nova_poshta/create_data/city_data/city_dov.json"

    def saveCity(self, data):
        fl_cl.save_file_json(self.file_json, data)

    def searchCity(self, data):
        if ""
        for
        bufer = {
            "CityName": '',
            "CityRef": '',
            "Page": '',
            "Limit": "50",
            "Language": "UA",
            "TypeOfWarehouseRef": '',
            "WarehouseId": '',
            "FindByString": ''
        }
        resp = np_cl.get_search_warhouse(bufer)
        self.saveCity(resp)




