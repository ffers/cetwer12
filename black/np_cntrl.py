from api.nova_poshta.create_data import WarehouseRefCl, NpClient
from server_flask.db import db
import re

war_cl = WarehouseRefCl()
np_cl_api = NpClient()


class NpCntrl:
    def __init__(self):
        self.data = {}
        self.np_api = NpClient()

    def manager_data(self, order):
        self.runup_recepient(order)
        print(self.data)
        resp = np_cl_api.runup_doc(self.data)
        return resp

    def runup_recepient(self, order):
        data = self.parse_data(order)
        self.back_delivery(data)
        self.option_set(data)
        self.recipient_create(data)
        self.contact_recipient(data)
        print(f"runup {data}")
      

    def strip_phone(self, phone):
        return re.sub(r"\D", "", phone)

    def parse_data(self, order):
        print(f"data order {vars(order)}")
        self.data.clear()
        info_ref = self.cityref_for_warehouseref(order.warehouse_ref)
        self.data.update(
            {
                "order_id": order.id,
                "description": order.description,
                "CityRecipient": info_ref.get("CityRef"),
                "RecipientAddress": order.warehouse_ref,
                "payment_option": order.payment_method_id,
                "RecipientsPhone": self.strip_phone(order.phone),
                "FirstName": order.recipient.first_name,
                "LastName": order.recipient.last_name,
                "MiddleName": order.recipient.second_name,
                "Email": "test@i.com",
                "TypeOfWarehouse": info_ref.get("TypeOfWarehouse"),
                "warehouse_method_id": order.warehouse_method_id,
                "warehouse_option": order.warehouse_option,
                "Cost": order.sum_price,
                "BackwardDeliveryData": None,
                "OptionsSeat": None,
                "Description": f"Одяг Jemis {order.order_code}",
            }
        )
        print(order.payment_method_id)
        if self.data["payment_option"] == 3:
            self.data.update({"sum_before_goods": order.sum_before_goods})
        print(self.data)
        return self.data

    def back_delivery(self, data):
        if 1 == data["payment_option"]:
            data.update({"AfterpaymentOnGoodsCost": data["Cost"]})
        if 3 == data["payment_option"]:
            data.update(
                {"AfterpaymentOnGoodsCost": data["Cost"] - data["sum_before_goods"]}
            )
        return data

    def option_set(self, data):
        print(f"проверяєм адрес {data}")
        poshtomat ="f9316480-5f2d-425d-bc2c-ac7cd29decf0"
        if data.get("TypeOfWarehouse") == poshtomat:
            data.update(
                {
                    "OptionsSeat": [
                        {
                            "volumetricVolume": "1",
                            "volumetricWidth": "10",
                            "volumetricLength": "10",
                            "volumetricHeight": "10",
                            "weight": "1",
                        }
                    ]
                }
            )
        return data

    def recipient_create(self, data):
        ref = np_cl_api.create_contragent(data)
        print(f"Recipient {ref}")
        data.update({"Recipient": ref})
        return data

    def contact_recipient(self, data):
        ref = np_cl_api.create_contact(data)
        print(f"ContactRecipient {ref}")
        data.update({"ContactRecipient": ref})
        return data

    def cityref_for_warehouseref(self, warehouse_ref):
        resp = self.np_api.get_s_war_ref(warehouse_ref)
        print("dev_cityref_for_warehouseref: ", resp)
        if resp["success"]:
            return resp["data"][0]
        resp_dict = {
            "success": True,
            "data": [
                {
                    "SiteKey": "27487",
                    "Description": "Пункт приймання-видачі (до 30 кг): вул. Котляревької, 15/2",
                    "DescriptionRu": "Пункт приема-выдачи (до 30 кг), ул. Котляревской, 15/2",
                    "ShortAddress": "Демурине, Котляревької, 15/2",
                    "ShortAddressRu": "Демурино, Котляревской, 15/2",
                    "Phone": "380800500609",
                    "TypeOfWarehouse": "841339c7-591a-42e2-8233-7a0a00f0ed6f",
                    "Ref": "95072367-ca72-11ea-b39d-b8830365bd14",
                    "Number": "1",
                    "CityRef": "36b14e18-c76d-11ea-a970-b8830365ade4",
                    "CityDescription": "Демурине",
                    "CityDescriptionRu": "Демурино",
                    "SettlementRef": "0de51520-4b3a-11e4-ab6d-005056801329",
                    "SettlementDescription": "Демурине",
                    "SettlementAreaDescription": "Дніпропетровська",
                    "SettlementRegionsDescription": "Межівський",
                    "SettlementTypeDescription": "селище міського типу",
                    "SettlementTypeDescriptionRu": "поселок городского типа",
                    "Longitude": "36.475922000000000",
                    "Latitude": "48.180078000000000",
                    "PostFinance": "0",
                    "BicycleParking": "0",
                    "PaymentAccess": "0",
                    "POSTerminal": "0",
                    "InternationalShipping": "0",
                    "SelfServiceWorkplacesCount": "0",
                    "TotalMaxWeightAllowed": "30",
                    "PlaceMaxWeightAllowed": "0",
                    "SendingLimitationsOnDimensions": {
                        "Width": 120,
                        "Height": 120,
                        "Length": 120,
                    },
                    "ReceivingLimitationsOnDimensions": {
                        "Width": 120,
                        "Height": 120,
                        "Length": 120,
                    },
                    "Reception": {
                        "Monday": "09:00-19:00",
                        "Tuesday": "-",
                        "Wednesday": "09:00-19:00",
                        "Thursday": "09:00-16:00",
                        "Friday": "09:00-16:00",
                        "Saturday": "09:00-16:00",
                        "Sunday": "-",
                    },
                    "Delivery": {
                        "Monday": "09:00-15:10",
                        "Tuesday": "-",
                        "Wednesday": "09:00-15:10",
                        "Thursday": "09:00-15:10",
                        "Friday": "09:00-15:10",
                        "Saturday": "09:00-15:10",
                        "Sunday": "-",
                    },
                    "Schedule": {
                        "Monday": "09:00-16:00",
                        "Tuesday": "09:00-16:00",
                        "Wednesday": "09:00-16:00",
                        "Thursday": "09:00-16:00",
                        "Friday": "09:00-16:00",
                        "Saturday": "09:00-16:00",
                        "Sunday": "-",
                    },
                    "DistrictCode": "Ск Пок",
                    "WarehouseStatus": "Working",
                    "WarehouseStatusDate": "2024-03-06 00:00:00",
                    "WarehouseIllusha": "0",
                    "CategoryOfWarehouse": "Store",
                    "Direct": "",
                    "RegionCity": "ДНІПРО ПОСИЛКОВИЙ",
                    "WarehouseForAgent": "1",
                    "GeneratorEnabled": "0",
                    "MaxDeclaredCost": "15000",
                    "WorkInMobileAwis": "0",
                    "DenyToSelect": "0",
                    "CanGetMoneyTransfer": "0",
                    "HasMirror": "0",
                    "HasFittingRoom": "0",
                    "OnlyReceivingParcel": "0",
                    "PostMachineType": "",
                    "PostalCodeUA": "52921",
                    "WarehouseIndex": "3781/1",
                    "BeaconCode": "",
                    "Location": "",
                }
            ],
            "errors": [],
            "warnings": [],
            "info": {"totalCount": 1},
            "messageCodes": [],
            "errorCodes": [],
            "warningCodes": [],
            "infoCodes": [],
        }
        return False
