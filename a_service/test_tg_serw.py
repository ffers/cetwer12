import pytest
from .tg_serv import TgServ

def test_create_marketplace():
    tg = TgServ()
    assert tg.create_text_order("order") == True