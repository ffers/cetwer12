from repository import jour_ch_rep as rep
from a_service import jour_ch_serv as serv

class JourChCntrl:
    def add_(self, data):
        resp = rep.add_(data)
        return resp

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



jour_ch_cntrl = JourChCntrl()


#     id = db.Column(db.Integer, primary_key=True)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     status = db.Column(db.String(50))
#     quantity = db.Column(db.Integer)
#     body = db.Column(db.Numeric(precision=8, scale=2))
#     income = db.Column(db.Numeric(precision=8, scale=2))
#     product_id = db.Column(db.Integer, db.ForeignKey(
#         'product_source.id', name='fk_journal_change_product_source_id'))
#     product = db.relationship('ProductSource', backref='journal_change')