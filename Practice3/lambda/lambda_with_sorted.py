# 1. Сортировка товаров по цене
items = [("Cake", 4000), ("Bread", 200), ("Honey", 3500)]
by_price = sorted(items, key=lambda x: x[1])

# 2. Сортировка имен по длине
students = ["Sanzhar", "Ali", "Baurzhan", "Aziza"]
by_len = sorted(students, key=lambda n: len(n))

# 3. Сортировка словарей по ID пользователя
users = [{"id": 105}, {"id": 101}, {"id": 103}]
by_id = sorted(users, key=lambda u: u["id"])

# 4. Сортировка по последней букве (для кодов)
codes = ["24B-A", "24B-C", "24B-B"]
sorted_codes = sorted(codes, key=lambda c: c[-1])

print(by_price)