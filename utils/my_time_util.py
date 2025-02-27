from datetime import datetime
from datetime import timezone

def my_time():
        yield datetime.now(timezone.utc)