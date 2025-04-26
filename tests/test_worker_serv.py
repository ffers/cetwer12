

from black.tg_answer_cntrl import OrderCntrl, SourAnCntrl, TelegramController, TgAnswerCntrl
from .lib.tg_lib import LibTG
from server_flask.flask_app import flask_app
import pytest

class TestWorker:
    await_button_tg = TgAnswerCntrl().await_tg_button
    
    def test_just_message(self):
        pointer = self.await_button_tg(LibTG.just_message)
        print(pointer)
        assert pointer.cmd == "just_message"

    def test_hashtag(self):
        pointer = self.await_button_tg(LibTG.message_hashtag)
        print(pointer)
        assert pointer.cmd == "unknown_command"
    
    def test_stock_stock_false(self):
        pointer = self.await_button_tg(LibTG.message_stock_stock_false)
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
            pointer = self.await_button_tg(LibTG.message_stock_courier)
            print(pointer)
            assert  pointer.chat == "courier"
            assert  pointer.cmd == "stock"
            assert  pointer.text == '‼️ Некоректний (комент)\nBX1: Нерахується\nBX3: 20\nBX4: 20\n'
            assert  pointer.reply == "Don`t have respone."
            assert  pointer.content[0].get("article") == "BX1"
            assert  pointer.resp == []
            assert  pointer.comment == None

    def test_take_courier(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(LibTG.message_take_courier)
            print(pointer)
            assert  pointer.chat == "courier"
            assert  pointer.cmd == "take_courier"
            assert  pointer.text == "Ярик отдал на покрас\n45W1: -50\n"
            assert  pointer.reply == "Don`t have respone."
            assert  pointer.content == [{'article': '45W1', 'pack': 1, 'quantity': -50, 'crm': True}]
            assert  pointer.resp == []
            assert  pointer.comment == 'Ярик отдал на покрас\n'

    def test_add_color_35_45(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(LibTG.add_color_35_45)
            print(pointer)
            assert  pointer.chat == "stock"
            assert  pointer.cmd == "stock"
            assert  pointer.text == "Додано Ярік\n35N: 48\n45N: 48\n"
            assert  pointer.reply == "Don`t have respone."
            assert  pointer.content == [{'article': '35N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}, 'quantity': 48, 'crm': True}, {'article': '45N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}, 'quantity': 48, 'crm': True}]
            assert  pointer.resp == []
            assert  pointer.comment == "Додано Ярік\n"

    def test_add_color_35(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(LibTG.add_color_35)
            print(pointer)
            assert  pointer.chat == "stock"
            assert  pointer.cmd == "stock"
            assert  pointer.text == "Додано Ярік\n35N: 48\n"
            assert  pointer.reply == "Don`t have respone."
            assert  pointer.content == [{'article': '35N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}, 'quantity': 48, 'crm': True}]
            assert  pointer.resp == []
            assert  pointer.comment == "Додано Ярік\n" 

    def test_add_color_45(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(LibTG.add_color_45)
            print(pointer)
            assert  pointer.chat == "stock"
            assert  pointer.cmd == "stock"
            assert  pointer.text == "Додано Ярік\n45N: 48\n"
            assert  pointer.reply == "Don`t have respone."
            assert  pointer.content == [{'article': '45N', 'data': {28: 12, 29: 12, 30: 12, 31: 12}, 'quantity': 48, 'crm': True}]
            assert  pointer.resp == []
            assert  pointer.comment == "Додано Ярік\n" 

    def test_take_color_35_45(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(LibTG.take_color_35_45)
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
            pointer = self.await_button_tg(LibTG.take_color_35)
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
            pointer = self.await_button_tg(LibTG.take_color_45)
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
            pointer = self.await_button_tg(LibTG.unknown_chat)
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
            pointer = self.await_button_tg(LibTG.callback_query_confirmation)
            print(pointer)
            assert "manager" ==  pointer.chat 
    
    def test_callback_query_prom(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(LibTG.callback_query_confirmation_prom)
            print(pointer)
            assert "manager" ==  pointer.chat 

    def test_reply_make_comment(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(LibTG.test_reply_make_comment)
            print(pointer)
            assert "manager" ==  pointer.chat 
            assert "reply_manager" == pointer.cmd
            assert "Denys" == pointer.author

    def test_reply_make_comment_false_chat(self):
        with flask_app.app_context():
            pointer = self.await_button_tg(LibTG.test_reply_make_comment_false)
            print(pointer)
            assert "np_delivery" ==  pointer.chat 
            assert "reply_to_message" == pointer.cmd

    def test_search_6_numbers(self):
        with flask_app.app_context():
            codes = ["ASX-351213", "R-841603966", 
                     "318724837", "P-337489755"]
            data = LibTG.test_search_6_numbers
            resp = []
            for code in codes:
                data["message"]["text"] = code
                resp.append(self.await_button_tg(data))
                print("Assert", resp)
            assert len(resp) == 4  # 4 ChatData

            assert resp[0].cmd == "search_order_manager"
            assert "PROM Замовлення № ASX-351213" in resp[0].text

            assert resp[1].content[0].id == 2500
            assert "ROZETKA" in resp[1].text

            assert resp[3].content == []  # останній — без замовлень
            assert "Немає замовлень" in resp[3].text

                



    # def test_two(self):
    #     assert self.value == 1