import datetime

# 1: Subtract five days from the current date 
# datetime.datetime.now() gets the current date and precise time from your computer.
current_date = datetime.datetime.now()

# datetime.timedelta is used for "date math" (adding and subtracting days, hours, etc.).
five_days_ago = current_date - datetime.timedelta(days=5)

# .strftime("%Y-%m-%d") converts the date object into a readable string (Year-Month-Day).
print("Current Date:", current_date.strftime("%Y-%m-%d"))
print("Five days ago:", five_days_ago.strftime("%Y-%m-%d"))

print("-" * 30)

# 2: Print yesterday, today, tomorrow 
today = datetime.datetime.now()

# Subtract 1 day using timedelta to get yesterday's date.
yesterday = today - datetime.timedelta(days=1)

# Add 1 day to get tomorrow's date.
tomorrow = today + datetime.timedelta(days=1)

print("Yesterday:", yesterday.strftime("%Y-%m-%d"))
print("Today:    ", today.strftime("%Y-%m-%d"))
print("Tomorrow: ", tomorrow.strftime("%Y-%m-%d"))

print("-" * 30)

# 3: Drop microseconds from the time
dt_with_microseconds = datetime.datetime.now()

# The .replace(microsecond=0) method creates a copy of the date but zeros out the microseconds.
dt_without_microseconds = dt_with_microseconds.replace(microsecond=0)

print("With microseconds:    ", dt_with_microseconds)
print("Without microseconds: ", dt_without_microseconds)

print("-" * 30)

# 4: Calculate the difference between two dates in seconds
# Create two specific points in time (e.g., today and tomorrow at noon).
date1 = datetime.datetime(2026, 2, 20, 12, 0, 0) 
date2 = datetime.datetime(2026, 2, 21, 12, 0, 0) 

# Subtracting one date from another results in a 'timedelta' object (duration).
difference = date2 - date1

# .total_seconds() converts the entire difference (days, hours, minutes) into a single number — seconds.
# This is useful for IT and networking interests to measure delays or server uptime.
seconds_diff = difference.total_seconds()

print(f"Difference between {date1} and {date2}:")
print(f"{seconds_diff} seconds")