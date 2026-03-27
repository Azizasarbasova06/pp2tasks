# 1. Поиск дорогих товаров (> 5000)
prices = [1200, 6000, 300, 15000, 4500]
expensive = list(filter(lambda p: p > 5000, prices))

# 2. Сортировка городов только на 'A'
cities = ["Almaty", "Atyrau", "Astana", "Shymkent", "Aktau"]
a_cities = list(filter(lambda c: c.startswith("A"), cities))

# 3. Только проходные баллы
scores = [45, 88, 32, 90, 50, 49]
passed = list(filter(lambda s: s >= 50, scores))

# 4. Удаление пустых заказов
orders = ["Cake", "", "Bread", " ", "Honey"]
valid = list(filter(lambda x: x.strip(), orders))

print(a_cities)