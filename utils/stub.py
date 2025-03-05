import os

class Stub:
    def __init__(self):
        self.env = os.getenv("ENV")

    def status_order_load(self):
        if self.env == "dev":
            return 5 
        else:
            return 1

