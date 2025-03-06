
from a_service import ResponceDirector
from black.tg_answer_cntrl import OrderCntrl, SourAnCntrl, TelegramController
from .lib.lib import Lib


class TestClassDemoInstance:

    responce = ResponceDirector()
    
    def test_just_message(self):
        pointer = self.responce.construct(Lib.just_message, OrderCntrl, SourAnCntrl, TelegramController)
        print(pointer)
        assert pointer.cmd == "just_message"
    
    def test_stock_stock(self):
        pointer = self.responce.construct(Lib.message_stock_stock, OrderCntrl, SourAnCntrl, TelegramController)
        print(pointer)
        assert  pointer.chat == "stock"
        assert  pointer.cmd == "stock"
        assert  pointer.text == "#склад (Игорь): 35N10: 25(300) 45N10: 25(300)"
        assert  pointer.reply == "Don`t have respone."
        assert  pointer.content == []
        assert  pointer.resp == []
        assert  pointer.comment == "Игорь\n"


    # def test_two(self):
    #     assert self.value == 1