import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from black.marketplace_cntrl import MarketFactory
from api import EvoClient

def test_create_marketplace():
    market = MarketFactory.factory("prom")
    assert isinstance(market, EvoClient)

# def test_create_unknown_marketplace():
#     market = MarketFactory.factory("unknown")
#     assert market is None 


# def test_create_marketplace_invalid():
#     with pytest.raises(ValueError, match="Неизвестный маркетплейс"):
#         MarketFactory.factory("invalid")
