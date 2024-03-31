from server_flask.models import Orders


class TTN_to_Prom():
    def main(self, order):

        if order.source_order_id == 2:
            invoice_ttn = order.ttn
            order_id_sources = order.order_id_sources
            return invoice_ttn, order_id_sources
        else:
            return None, None