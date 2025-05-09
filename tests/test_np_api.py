from black.tg_answer_cntrl import OrderCntrl
from .lib.tg_lib import LibTG
from server_flask.flask_app import flask_app


class TestRozet:
    order_cntrl = OrderCntrl()

    def test_create_ttn_np(self):
        with flask_app.app_context():
            order = self.order_cntrl.load_for_order_id(2476)
            resp = self.order_cntrl.del_method_np(order) 
            assert (True, '') == resp


    def test_create_registr(self):
        resp_np = {'ref_registr': '7be90718-2cf3-11f0-a1d5-48df37b921da', 'number_registr': '105-64378242'}