from repository import  ProductAnaliticRep
from repository import DayAnaliticRep
from service_asx.analitic import DayAnaliticServ

d_serv = DayAnaliticServ()
d_an = DayAnaliticRep()
pr_an = ProductAnaliticRep()

class DayAnalitic:
    def main(self):
        torg = pr_an.get_money_sale_day()
        return torg
