import logging

OC_log = logging.getLogger("order_cntrl")
OC_log.info("працює np_serv")
class NpServ:
    def create_address_dict_np(self, data):
        data_address = data["data"][0]
        address_dict_np = {
            "CityRef": data_address["CityRef"],
            "WarehouseMethod": self.add_warehouse_method(data_address),
            "CityName": data_address["CityDescription"],
            "WarehouseText": data_address["Description"],
            "WarehouseRef": data_address["Ref"]
        }
        return address_dict_np

    def examine_address_prom(self, data):
        # OC_log.info(f"delivery_provider_data {data}")
        war_ref = data["delivery_provider_data"]["recipient_warehouse_id"]
        if not war_ref:
            return False
        return war_ref

    def add_warehouse_method(self, address_dict):
        if address_dict["TypeOfWarehouse"] == "f9316480-5f2d-425d-bc2c-ac7cd29decf0":
            dict_warehouse = 2
        else:
            dict_warehouse = 1
        return dict_warehouse
