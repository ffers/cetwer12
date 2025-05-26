

from .base import Source


class DifferenceServ(Source):

    def load_source_difference_id_period(self, id, period, days):
        start_time, stop_time = self.ctx.w_time.load_work_time(period, days)
        
        product = self.ctx.diff_rep.load_source_difference_id_period(
            id, start_time, stop_time 
            )
        print(start_time, stop_time, "month")
        return product


