from api.nova_poshta.create_data import WarehouseRefCl, NpClient
from server_flask.models import Orders
from server_flask.db import db

war_cl = WarehouseRefCl()
np_cl = NpClient()


class NpCabinetCl():
    def __init__(self):
        self.data = {}

    def manager_data(self, order):
        self.runup_recepient(order)
        print(self.data)
        resp = np_cl.runup_doc(self.data)
        self.add_ttn_crm(resp, order)
        return resp

    def add_ttn_crm(self, resp, order):
        order.ttn = resp["data"][0]["IntDocNumber"]
        db.session.commit()

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
                "Description": "Одяг Jemis"
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
        ref = np_cl.create_contragent(data)
        print(f"Recipient {ref}")
        data.update({
            "Recipient": ref
        })
        return data

    def contact_recipient(self, data):
        ref = np_cl.create_contact(data)
        print(f"ContactRecipient {ref}")
        data.update({
            "ContactRecipient": ref
        })
        return data

    def runup_recepient(self, order):
        data = self.parse_data(order)
        self.back_delivery(data)
        self.option_set(data)
        self.recipient_create(data)
        self.contact_recipient(data)
        print(f"runup {data}")
        pass








    # def manager_data(self, order):
    #     buffer = create_data_np(order)
    #     RecipientAddress = None
    #     RecipientAddress = ware.RefWarehouse(order)
    #     RecipientContact = search_contact_Ref(buffer, order)
    #     Recipient = get_create_contragent(json_read_dict(json_data_np_dict), buffer)
    #     date_time = time_now()
    #     next_time = next(date_time)
    #     test_time = next_time.strftime("%d.%m.%Y")
    #     SUN.update({"RecipientAddress": RecipientAddress, "Recipient": Recipient, "ContactRecipient": RecipientContact,
    #                 "DateTime": test_time})
    #     search_money(order)
    #     created_ttn = get_generate_doc(json_read_dict(json_data_np_dict), SUN)




    # def manager_data(self, order):
    #     buffer = create_data_np(order)
    #     RecipientAddress = None
    #     RecipientAddress = ware.RefWarehouse(order)
    #     RecipientContact = search_contact_Ref(buffer, order)
    #     Recipient = get_create_contragent(json_read_dict(json_data_np_dict), buffer)
    #     date_time = time_now()
    #     next_time = next(date_time)
    #     test_time = next_time.strftime("%d.%m.%Y")
    #     SUN.update({"RecipientAddress": RecipientAddress, "Recipient": Recipient, "ContactRecipient": RecipientContact,
    #                 "DateTime": test_time})
    #     search_money(order)
    #     created_ttn = get_generate_doc(json_read_dict(json_data_np_dict), SUN)
