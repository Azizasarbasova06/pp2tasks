# 1. Квадрат числа
sq = lambda x: x * x
# 2. Сложение
plus = lambda a, b: a + b
# 3. Проверка на четность
is_even = lambda x: x % 2 == 0
# 4. Склеивание строк
full_name = lambda f, l: f"{f} {l}"

print(sq(4), plus(2, 3), is_even(5), full_name("Ali", "B"))