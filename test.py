from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, timezone


def my_time():
        yield datetime.now(timezone.utc)

def make_v2(shifttime=13, zone="Europe/Kyiv"):
        current_time = next(my_time()).astimezone(ZoneInfo(zone))
        print('current_time:', current_time)
        start_time = current_time - timedelta(hours=shifttime)
        print('start_time:', start_time)
        zone_tz = start_time.replace(hour=shifttime, 
                    minute=0, second=0, microsecond=0
        )
        print('zone_tz:', zone_tz)
        utc_clean = zone_tz.astimezone(timezone.utc)
        print('utc_clean:', utc_clean)
        return utc_clean

make_v2()