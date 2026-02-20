import datetime

# --- Task 1: Subtract five days from current date ---
current_date = datetime.datetime.now()
five_days_ago = current_date - datetime.timedelta(days=5)
print("Current Date:", current_date.strftime("%Y-%m-%d"))
print("Five days ago:", five_days_ago.strftime("%Y-%m-%d"))

print("-" * 30)

# --- Task 2: Print yesterday, today, tomorrow ---
today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

print("Yesterday:", yesterday.strftime("%Y-%m-%d"))
print("Today:    ", today.strftime("%Y-%m-%d"))
print("Tomorrow: ", tomorrow.strftime("%Y-%m-%d"))

print("-" * 30)

# --- Task 3: Drop microseconds from datetime ---
# Мы используем метод .replace(), чтобы обнулить микросекунды
dt_with_microseconds = datetime.datetime.now()
dt_without_microseconds = dt_with_microseconds.replace(microsecond=0)

print("With microseconds:   ", dt_with_microseconds)
print("Without microseconds:", dt_without_microseconds)

print("-" * 30)

# --- Task 4: Calculate two date difference in seconds ---
date1 = datetime.datetime(2026, 2, 20, 12, 0, 0) # Сегодня полдень
date2 = datetime.datetime(2026, 2, 21, 12, 0, 0) # Завтра полдень

# Разница дает объект timedelta
difference = date2 - date1
seconds_diff = difference.total_seconds()

print(f"Difference between {date1} and {date2}:")
print(f"{seconds_diff} seconds")