import logging

OC_log = logging.getLogger("order_cntrl")

class NpServ:
    def create_address_dict_np(self, data_address):
        address_dict_np = {
            "CityRef": data_address["CityRef"],
            "TypeWarehouse": data_address["TypeOfWarehouse"],
            "CityName": data_address["CityDescription"],
            "WarehouseText": data_address["Description"],
            "WarehouseRef": data_address["Ref"]
        }
        return address_dict_np

    def examine_address_prom(self, data):
        war_ref = data["delivery_provider_data"]["recipient_warehouse_id"]
        if not war_ref:
            return False
        return war_ref

    def add_warehouse_method(self, address_dict):
        if address_dict["TypeWarehouse"] == "f9316480-5f2d-425d-bc2c-ac7cd29decf0":
            dict_warehouse = {"warehouse_method": 2}
        else:
            dict_warehouse = {"warehouse_method": 1}
        return dict_warehouse
