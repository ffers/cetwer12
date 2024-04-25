from datetime import datetime, timedelta
class WorkTimeCntrl:

    def my_time(self):
        yield (datetime.utcnow())

    def load_work_time(self, period):
        start_time, stop_time = None, None
        if period == "day":
            start_time, stop_time = self.day()
        elif period == "week":
            start_time, stop_time = self.week()
        elif period == "month":
            start_time, stop_time = self.month()
        elif period == "year":
            start_time, stop_time = self.year()
        elif period == "all":
            start_time, stop_time = self.all()
        return start_time, stop_time

    def day(self):
        current_time = next(self.my_time())
        start_time = current_time - timedelta(hours=14)
        start_time = start_time.replace(hour=14, minute=0, second=0,
                                        microsecond=0)
        stop_time = start_time + timedelta(days=1)
        return start_time, stop_time

    def week(self):
        current_time = next(self.my_time())
        start_time = current_time - timedelta(hours=14)
        start_time = start_time.replace(hour=14, minute=0, second=0,
                                        microsecond=0)
        current_week_day = start_time.weekday()
        # Визначаємо перший день поточного тижня (понеділок)
        first_day_of_week = start_time - timedelta(days=current_week_day)
        last_day_of_week = first_day_of_week + timedelta(weeks=1)
        return first_day_of_week, last_day_of_week

    def month(self):
        current_time = next(self.my_time())
        start_time = current_time - timedelta(hours=14)
        start_time = start_time.replace(day=1, hour=14, minute=0, second=0,
                                        microsecond=0)
        next_month = start_time.replace(day=28) + timedelta(days=4)
        stop_time = next_month - timedelta(days=next_month.day)
        return start_time, stop_time

    def year(self):
        current_time = next(self.my_time())
        start_time = current_time - timedelta(hours=14)
        start_time = start_time.replace(month=1, day=1, hour=14, minute=0, second=0,
                                        microsecond=0)
        stop_time = datetime(current_time.year, 12, 31)
        return start_time, stop_time

    def all(self):
        current_time = next(self.my_time()) + timedelta(hours=1)
        return "2021-04-25 13:47:10.560329", current_time





