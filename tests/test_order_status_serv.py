import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from a_service import Status


def test_make_procces():
    market = Status.update_order("1", 7)
    assert market is True