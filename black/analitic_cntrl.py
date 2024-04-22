from repository import an_rep as rep
from a_service import an_serv as serv

class AnCntrl:
    # def main(self):
    #     torg = prod_an_rep.get_money_sale_day()
    #     return torg

    def add_(self, args):
        print(args)
        resp = rep.add_(args)
        return resp

    def update_(self, id, args):
        return rep.update_(id, args)

    def load_all(self):
        resp = rep.load_all()
        return resp

    def load_period(self, period):
        resp = rep.load_period(period)
        return resp

    def load_day(self):
        return rep.load_day()

    # def update_(self, id, req):
    #     data = prod_serv.add_product_source(req)
    #     resp = prod_rep.update_product_source(id, data)
    #     return resp
    #
    # def load_all(self):
    #     data = prod_rep.load_product_source_all()
    #     return data
    #
    # def load_item(self, product_id):
    #     resp = prod_rep.load_product_source_item(product_id)
    #     return resp
    #
    # def update_quan(self, id, quantity):
    #     resp = prod_rep.update_prod_sour_quan(id, quantity)
    #     return resp
    #
    #
    # def load_article(self, article):
    #     item = prod_rep.load_product_source_article(article)
    #     return item
    #
    # def delete_(self, id):
    #     bool = prod_rep.delete_product_source(id)
    #     return bool



an_cntrl = AnCntrl()
#
# id = db.Column(db.Integer, primary_key=True)
# timestamp = db.Column(db.DateTime, default=datetime.utcnow)
# period = db.Column(db.String(50))
# torg = db.Column(db.Numeric(precision=8, scale=2))
# body = db.Column(db.Numeric(precision=8, scale=2))
# worker = db.Column(db.Numeric(precision=8, scale=2))
# prom = db.Column(db.Numeric(precision=8, scale=2))
# orders = db.Column(db.Integer)
# rozet = db.Column(db.Numeric(precision=8, scale=2))
# google_shop = db.Column(db.Numeric(precision=8, scale=2))
# insta = db.Column(db.Numeric(precision=8, scale=2))
# profit = db.Column(db.Numeric(precision=8, scale=2))
# balance = db.Column(db.Numeric(precision=8, scale=2))
# wait = db.Column(db.Numeric(precision=8, scale=2))
# stock = db.Column(db.Numeric(precision=8, scale=2))
# income = db.Column(db.Numeric(precision=8, scale=2))
# inwork = db.Column(db.Numeric(precision=8, scale=2))
# salary = db.Column(db.Numeric(precision=8, scale=2))