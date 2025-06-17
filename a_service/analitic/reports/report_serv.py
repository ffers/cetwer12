


from utils import DEBUG

from ..base import Handler


'''
Зараз у мене є кілька віжповідачів на запрос про аналітику
Але потрібно зробити щоб було легше все запрос про аналітику у різні часи
підрахунок усього та окрремо репорт та інше що мені потрібно
'''

class ReportServ(Handler):
    def send_report(self):
        try:
            self.ctx.source_an_cntrl.add_quantity_crm_today()
            self.ctx.ord_cntrl.change_status_roz()
            text = "#quan 35N, 45N, 35W1, 45W1, 35N10, 40N10, 45N10, BX1, BX2, BX3, BX4, BX5, 35N11, 40N11, 45N11, 35W, 45W, 35W13, 45W13"
            self.ctx.tg_cash.quan_f(text)
            return True
        except Exception as e:
            if DEBUG >= 5: print(f'send_report {e}')
            self.ctx.logger.exception(f'send_report {e}')
            raise       

    def diff_count_sold(self):
        return self.ctx.source_an_cntrl.sour_diff_all_source_sold("two_days") 
