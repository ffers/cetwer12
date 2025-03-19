

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
        assert  pointer.comment == None

    def test_stock_courier(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.message_stock_courier)
            print(pointer)
            assert  pointer.chat == "courier"
            assert  pointer.cmd == "stock"
            assert  pointer.text == "Игорь\n35N10: 300\n45N10: 300\n"
            assert  pointer.reply == "Don`t have respone."
            assert  pointer.content == [{'article': '35N10', 'pack': 25, 'quantity': 300}, {'article': '45N10', 'pack': 25, 'quantity': 300}]
            assert  pointer.resp == [{'article': '35N10', 'quantity': 300}, {'article': '45N10', 'quantity': 300}]
            assert  pointer.comment == 'Игорь\n'

    def test_take_courier(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.message_take_courier)
            print(pointer)
            assert  pointer.chat == "courier"
            assert  pointer.cmd == "take_courier"
            assert  pointer.text == "Ярик отдал на покрас\n45W1: -50\n"
            assert  pointer.reply == "Don`t have respone."
            assert  pointer.content == [{'article': '45W1', 'pack': 1, 'quantity': 50}]
            assert  pointer.resp == [{'article': '45W1', 'quantity': -50}]
            assert  pointer.comment == 'Ярик отдал на покрас\n'

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

    def test_take_color_35_45(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.take_color_35_45)
            print(pointer)
            assert  pointer.chat == "stock"
            assert  pointer.cmd == "take"
            # assert  pointer.text == "Додано Ярік\n35N: 48\n45N: 48\n"
            # assert  pointer.reply == "Don`t have respone."
            # assert  pointer.content == [{'article': '35N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}}, {'article': '45N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}}]
            # assert  pointer.resp == [{'article': '35N', 'quantity': 48}, {'article': '45N', 'quantity': 48}]
            # assert  pointer.comment == "Додано Ярік\n"

    def test_take_color_35(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.take_color_35)
            print(pointer)
            assert  pointer.chat == "stock"
            assert  pointer.cmd == "take"
            # assert  pointer.text == "Додано Ярік\n35N: 48\n"
            # assert  pointer.reply == "Don`t have respone."
            # assert  pointer.content == [{'article': '35N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}}]
            # assert  pointer.resp == [{'article': '35N', 'quantity': 48}]
            # assert  pointer.comment == "Додано Ярік\n" 

    def test_take_color_45(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.take_color_45)
            print(pointer)
            assert  pointer.chat == "stock"
            assert  pointer.cmd == "take"
            # assert  pointer.text == "Додано Ярік\n45N: 48\n"
            # assert  pointer.reply == "Don`t have respone."
            # assert  pointer.content == [{'article': '45N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}}]
            # assert  pointer.resp == [{'article': '45N', 'quantity': 48}]
            # assert  pointer.comment == "Додано Ярік\n" 


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

    def test_callback_query_rozet(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.callback_query_confirmation)
            print(pointer)
            assert "manager" ==  pointer.chat 
    
    def test_callback_query_prom(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.callback_query_confirmation_prom)
            print(pointer)
            assert "manager" ==  pointer.chat 

    def test_reply_make_comment(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.test_reply_make_comment)
            print(pointer)
            assert "manager" ==  pointer.chat 
            assert "reply_manager" == pointer.cmd
            assert "Denys" == pointer.author

    def test_reply_make_comment_false_chat(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(Lib.test_reply_make_comment_false)
            print(pointer)
            assert "np_delivery" ==  pointer.chat 
            assert "reply_to_message" == pointer.cmd



    # def test_two(self):
    #     assert self.value == 1