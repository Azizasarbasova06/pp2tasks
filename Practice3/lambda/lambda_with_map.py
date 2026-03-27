# 1. Конвертация цен из KZT в USD (курс 450)
kzt = [1000, 4500, 9000]
usd = list(map(lambda x: x / 450, kzt))

# 2. Форматирование имен для БД
raw_names = ["ali", "BAUR", "aziza"]
fixed_names = list(map(lambda n: n.capitalize(), raw_names))

# 3. Вычисление площади квадратов из списка сторон
sides = [2, 5, 10]
areas = list(map(lambda s: s**2, sides))

# 4. Извлечение первого слова из описания
descr = ["IS major", "CS minor", "EC student"]
majors = list(map(lambda d: d.split()[0], descr))

print(fixed_names)