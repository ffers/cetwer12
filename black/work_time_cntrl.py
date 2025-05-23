from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, timezone
from utils import DEBUG


class WorkTimeCntrl:
    def __init__(self, shifttime=17, zone="Europe/Kyiv"):
        self.close_shift_utc = datetime.fromisoformat('2022-01-01T08:00').replace(tzinfo=ZoneInfo("Europe/Kyiv"))
        self.shifttime = shifttime
        self.zone = zone


    
    def start_utc_by_zone(self):
        current_time = next(self.my_time()).astimezone(ZoneInfo(self.zone))
        if DEBUG>5: print('current_time:', current_time)
        start_time = current_time - timedelta(hours=self.shifttime)
        zone_tz = start_time.replace(hour=self.shifttime, 
                    minute=0, second=0, microsecond=0,
                    tzinfo=ZoneInfo(self.zone)
        )
        utc_clean = zone_tz.astimezone(timezone.utc)
        if DEBUG>5: print('utc_clean:', utc_clean)
        return utc_clean


    def my_time(self):
        yield datetime.now(timezone.utc)

    def load_work_time(self, period, quantity=None):
        start_time, stop_time = None, None
        if period == "day":
            start_time, stop_time = self.day()
        elif period == "two_days":
            start_time, stop_time = self.two_day()
        elif period == "days":
            start_time, stop_time = self.days(quantity)
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
        start_time = self.start_utc_by_zone()
        stop_time = start_time + timedelta(days=1)
        return start_time, stop_time
    
    def days(self, quantity):
        start_time = self.start_utc_by_zone()
        stop_time = start_time + timedelta(days=quantity)
        return start_time, stop_time
    
    def two_day(self):
        start_time = self.start_utc_by_zone()
        start_time = start_time - timedelta(days=2) 
        stop_time = start_time + timedelta(days=2)
        return start_time, stop_time

    def week(self):
        start_time = self.start_utc_by_zone()
        current_week_day = start_time.weekday()
        # Визначаємо перший день поточного тижня (понеділок)
        first_day_of_week = start_time - timedelta(days=current_week_day)
        last_day_of_week = first_day_of_week + timedelta(weeks=1)
        return first_day_of_week, last_day_of_week

    def month(self):
        start_time = self.start_utc_by_zone()
        next_month = start_time.replace(day=28) + timedelta(days=4)
        stop_time = next_month - timedelta(days=next_month.day)
        return start_time, stop_time

    def year(self):
        current_time = next(self.my_time())
        start_time = self.start_utc_by_zone()
        stop_time = datetime(current_time.year, 12, 31)
        return start_time, stop_time

    def all(self):
        current_time = next(self.my_time()) + timedelta(hours=17)
        return "2021-04-25 17:47:10.560329", current_time





