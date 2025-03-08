

from black.tg_answer_cntrl import OrderCntrl, SourAnCntrl, TelegramController, TgAnswerCntrl
from .lib.lib import Lib
from server_flask.flask_app import flask_app


class TestClassDemoInstance:
    await_button_tg = TgAnswerCntrl().await_tg_button
    
    def test_just_message(self):
        pointer = self.await_button_tg(Lib.just_message)
        print(pointer)
        assert pointer.cmd == "just_message"

    def test_hashtag(self):
        pointer = self.await_button_tg(Lib.message_hashtag)
        print(pointer)
        assert pointer.cmd == "unknown_command"
    
    def test_stock_stock_false(self):
        pointer = self.await_button_tg(Lib.message_stock_stock_false)
        print(pointer)
        assert  pointer.chat == "stock"
        assert  pointer.cmd == "stock"
        assert  pointer.text == "#склад (Игорь): 35N10: 25(300) 45N10: 25(300)"
        assert  pointer.reply == "Don`t have respone."
        assert  pointer.content == []
        assert  pointer.resp == []
        assert  pointer.comment == "Игорь\n"

    def test_add_color_35_45(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.add_color_35_45)
            print(pointer)
            assert  pointer.chat == "stock"
            assert  pointer.cmd == "stock"
            assert  pointer.text == "Додано Ярік\n35N: 48\n45N: 48\n"
            assert  pointer.reply == "Don`t have respone."
            assert  pointer.content == [{'article': '35N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}}, {'article': '45N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}}]
            assert  pointer.resp == [{'article': '35N', 'quantity': 48}, {'article': '45N', 'quantity': 48}]
            assert  pointer.comment == "Додано Ярік\n"
    
    def test_comand_just(self):
        assert  2 == 2

    def test_add_color_35(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.add_color_35)
            print(pointer)
            assert  pointer.chat == "stock"
            assert  pointer.cmd == "stock"
            assert  pointer.text == "Додано Ярік\n35N: 48\n"
            assert  pointer.reply == "Don`t have respone."
            assert  pointer.content == [{'article': '35N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}}]
            assert  pointer.resp == [{'article': '35N', 'quantity': 48}]
            assert  pointer.comment == "Додано Ярік\n" 

    def test_add_color_45(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.add_color_45)
            print(pointer)
            assert  pointer.chat == "stock"
            assert  pointer.cmd == "stock"
            assert  pointer.text == "Додано Ярік\n45N: 48\n"
            assert  pointer.reply == "Don`t have respone."
            assert  pointer.content == [{'article': '45N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}}]
            assert  pointer.resp == [{'article': '45N', 'quantity': 48}]
            assert  pointer.comment == "Додано Ярік\n" 


    def test_unknown_chat_unknown_command(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.unknown_chat)
            print(pointer)
            assert "unknown_chat" ==  pointer.chat 
            # assert  pointer.cmd == "stock"
            # assert  pointer.text == "Додано 45N: 48\n"
            # assert  pointer.reply == "Don`t have respone."
            # assert  pointer.content == [{'article': '45N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}}]
            # assert  pointer.resp == [{'article': '45N', 'quantity': 48}]
            # assert  pointer.comment == "Додано Ярік\n" 

    def test_callback_query(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.callback_query_confirmation)
            print(pointer)
            assert "manager" ==  pointer.chat 

    def test_reply_make_comment(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.test_reply_make_comment)
            print(pointer)
            assert "manager" ==  pointer.chat 


    # def test_two(self):
    #     assert self.value == 1