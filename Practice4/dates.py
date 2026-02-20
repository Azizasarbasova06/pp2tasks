import datetime

# 1. Текущая дата и специфическое форматирование
now = datetime.datetime.now()
print("Current format:", now.strftime("%Y-%m-%d %H:%M:%S"))

# 2. Создание конкретного объекта даты
my_birthday = datetime.datetime(2006, 5, 15)
print("Birthday:", my_birthday.strftime("%A, %B %d, %Y"))

# 3. Вычисление разницы во времени (Timedelta)
today = datetime.datetime.now()
five_days_ago = today - datetime.timedelta(days=5)
print("5 days ago was:", five_days_ago)

# 4. Парсинг строки в дату (strptime)
date_str = "20 February, 2026"
date_obj = datetime.datetime.strptime(date_str, "%d %B, %Y")
print("Parsed date:", date_obj)