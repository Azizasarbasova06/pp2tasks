data = [1, 15, 20, 3, 50, 7]
# 1. Только больше 10
f1 = list(filter(lambda x: x > 10, data))
# 2. Только нечетные
f2 = list(filter(lambda x: x % 2 != 0, data))
# 3. Слова на букву 'A'
words = ["Apple", "Banana", "Atyrau", "Almaty"]
f3 = list(filter(lambda w: w.startswith("A"), words))
# 4. Только непустые строки
items = ["", "pen", " ", "notebook"]
f4 = list(filter(lambda x: x.strip() != "", items))

print(f1, f2, f3, f4)