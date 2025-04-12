from datetime import datetime
from datetime import timezone

def my_time():
        yield datetime.now(timezone.utc)

def my_time_v2():
    return next(my_time()).strftime("%m-%d-%Y %H:%M")

def my_time_v3():
    return next(my_time()).strftime("%d-%m-%Y %H:%M")