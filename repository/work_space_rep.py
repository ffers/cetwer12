from server_flask.models import PaymentMethod, DeliveryMethod, SourceOrder
from server_flask.db import db
from sqlalchemy import desc
from urllib.parse import unquote
from datetime import datetime, timedelta


class WorkSpaceRep:
    def __init__(self):
        pass

    def load_payment_methods(self):
        return PaymentMethod.query.all()
    
    def load_delivery_methods(self):
        return DeliveryMethod.query.all()
    
    def load_sources_order(self):
        return SourceOrder.query.all()
    