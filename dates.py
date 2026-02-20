#1
from datetime import datetime, timedelta

today = datetime.now()
five_days_ago = today - timedelta(days=5)

print("Current date:", today)
print("Date 5 days ago:", five_days_ago)

#2
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday.date())
print("Today:", today.date())
print("Tomorrow:", tomorrow.date())

#3
from datetime import datetime

now = datetime.now()
without_microseconds = now.replace(microsecond=0)

print("Current datetime:", now)
print("Without microseconds:", without_microseconds)

#4
from datetime import datetime

date1 = datetime(2026, 2, 20, 12, 0, 0)
date2 = datetime(2026, 2, 21, 12, 0, 0)

difference = date2 - date1
seconds = difference.total_seconds()

print("Difference in seconds:", seconds)