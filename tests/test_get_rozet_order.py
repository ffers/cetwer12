from black.tg_answer_cntrl import OrderCntrl
from .lib.lib import Lib
from server_flask.flask_app import flask_app


class TestRozet:
    order_cntrl = OrderCntrl()
    
    # def test_get_order(self):
    #     pointer = self.await_button_tg(Lib.just_message)
    #     print(pointer)
    #     assert pointer.cmd == "just_message"

