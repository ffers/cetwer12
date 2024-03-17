from service_asx.analitic import ProductAnanaliticServ

pr_an_cl = ProductAnanaliticServ()

class AnaliticControl():
    def product_analitic_cntrl(self, product_id):
        resp = pr_an_cl.main(product_id)
