# 1. Расчет скидки
discount = lambda p, d: p * (1 - d/100)

# 2. Проверка длины пароля
is_safe = lambda p: len(p) >= 8

# 3. Форматирование цены
fmt_price = lambda p: f"{p:,} тенге"

# 4. Полное имя пользователя
full_name = lambda f, l: f"{f.title()} {l.title()}"

print(fmt_price(5000000))
print(full_name("aziza", "s"))