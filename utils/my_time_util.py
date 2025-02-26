from datetime import datetime
from datetime import timezone

def my_time():
        yield datetime.now(timezone.utc).strftime("%a %b %d %Y %H:%M:%S")