import os

class Stub:
    def __init__(self):
        self.env = os.getenv("ENV")

    def status_order_load(self):
        if self.env == "dev":
            return 26
        else:
            return 1
        

d = os.getenv('DEBUG')
DEBUG = int(d) if d else 0

OSDEBUG = True if os.getenv('ENV') == 'dev' else False

     

