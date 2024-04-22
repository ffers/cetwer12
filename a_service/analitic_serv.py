


class DayAnaliticServ:
    def torg(self, item_all):
        torg = 0
        for item in item_all:
            if item.money_in_sale:
                torg = item.money_in_sale + torg
        return torg

an_serv = DayAnaliticServ()