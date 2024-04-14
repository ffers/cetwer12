from repository import  prod_an_rep
from repository import DayAnaliticRep
from a_service.analitic import DayAnaliticServ

d_serv = DayAnaliticServ()
d_an = DayAnaliticRep()


class DayAnalitic:
    def main(self):
        torg = prod_an_rep.get_money_sale_day()
        return torg
