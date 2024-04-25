from api.nova_poshta.create_data import WarehouseRefCl, NpClient
from server_flask.db import db

war_cl = WarehouseRefCl()
np_cl_api = NpClient()


class NpCntrl():
    def __init__(self):
        self.data = {}

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
        pass

    def parse_data(self, order):
        self.data.clear()
        self.data.update({
                "order_id": order.id,
                "description": order.description,
                "CityRecipient": order.city_ref,
                "RecipientAddress": order.warehouse_ref,
                "payment_option": order.payment_method_id,
                "RecipientsPhone": order.phone,
                "FirstName": order.client_firstname,
                "LastName": order.client_lastname,
                "MiddleName": order.client_surname,
                "Email": "test@i.com",
                "warehouse_option": order.warehouse_method_id,
                "Cost": order.sum_price,
                "BackwardDeliveryData": None,
                "OptionsSeat": None,
                "Description": f"Одяг Jemis {order.order_id_sources}"
        })
        print(order.payment_method_id)
        if self.data["payment_option"] == 3:
            self.data.update({"sum_before_goods": order.sum_before_goods})
        print(self.data)
        return self.data

    def back_delivery(self, data):
        if 1 == data["payment_option"]:
            data.update({"AfterpaymentOnGoodsCost": data["Cost"]})
        if 3 == data["payment_option"]:
            data.update({"AfterpaymentOnGoodsCost": data["Cost"] - data["sum_before_goods"]})
        return data

    def option_set(self, data):
        if 2 == data["warehouse_option"]:
            data.update({"OptionsSeat": [
            {
                "volumetricVolume": "0.2",
                "volumetricWidth": "10",
                "volumetricLength": "10",
                "volumetricHeight": "10",
                "weight": "0.2"
            }]})
        return data

    def recipient_create(self, data):
        ref = np_cl_api.create_contragent(data)
        print(f"Recipient {ref}")
        data.update({
            "Recipient": ref
        })
        return data

    def contact_recipient(self, data):
        ref = np_cl_api.create_contact(data)
        print(f"ContactRecipient {ref}")
        data.update({
            "ContactRecipient": ref
        })
        return data











