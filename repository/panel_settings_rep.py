from server_flask.models import PaymentMethod
from server_flask.db import db
from sqlalchemy import desc
from urllib.parse import unquote
from datetime import datetime, timedelta


class PanelSetRep:
    def __init__(self):
        pass

    def load_all(self):
        return PaymentMethod.query.all()
    