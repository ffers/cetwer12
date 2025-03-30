import logging
import pytest

@pytest.fixture(scope="session", autouse=True)
def disable_sqlalchemy_info():
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.orm").setLevel(logging.WARNING)
