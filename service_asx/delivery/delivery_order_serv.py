

class DeliveryOrderServ():
    def create_dict(self, first_data, order):
        data = first_data["data"][0]
        item = {
            "ref_ttn": data["Ref"],
            "number_ttn": data["IntDocNumber"],
            "ref_registr": None,
            "number_registr": "-",
            "order_id": order.id,
            "status_id": 1
        }
        return item

    def create_dict_reg(self, first_data):
        data = first_data["data"][0]
        item = {
            "ref_registr": data["Ref"],
            "number_registr": data["Number"],
        }
        return item

    def load_dict_order(self, data):
        print(data)
        order_id = data["id"]
        return order_id

    def create_list_ttn(self, items):
        list_data = []
        for item in items:   # взяти ордери створити ліст
            list_data.append(item.ref_ttn)
        return list_data



