import time
from datetime import datetime, timezone, timedelta

def time_now():
    while True:
        current_datetime = datetime.now(timezone.utc) + timedelta(hours=4)
        yield current_datetime
        time.sleep(1)
