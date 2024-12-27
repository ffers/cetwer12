



class MarketplaceServ:
    def create_status_get(self, order_id, status_order):
        dict_status_prom = None
        print(status_order)
        if 2 == status_order: # скасовано 
            dict_status_prom = {
                "status": "canceled",
                "ids": [order_id],
                "cancellation_reason": "not_available",
                "cancellation_text": "Не виходить дозвонитися"
            }
        if 1 == status_order: # прийнято
            dict_status_prom = {
                "status": "received",
                "ids": [order_id]
            }
        if 3 == status_order: # підтверженно
            dict_status_prom = {
                "custom_status_id": 137639,
                "ids": [order_id]
            }
        return dict_status_prom

    def dict_invoice(self, order_id, invoice, delivery):
        dict_ttn_prom = {
            "order_id": order_id,
            "declaration_id": invoice,
            "delivery_type": delivery
        }
        return dict_ttn_prom


prom_serv = PromServ()