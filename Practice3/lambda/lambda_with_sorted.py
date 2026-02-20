# 1. Сортировка списка кортежей по возрасту
people = [("Ali", 25), ("Baur", 18), ("Sanzhar", 22)]
s1 = sorted(people, key=lambda x: x[1])
# 2. Сортировка слов по длине
words = ["university", "is", "fun"]
s2 = sorted(words, key=lambda x: len(x))
# 3. Сортировка словаря по значению
prices = {"apple": 50, "orange": 30, "banana": 70}
s3 = sorted(prices.items(), key=lambda x: x[1])
# 4. Обратная сортировка по числам
nums = [5, 2, 9, 1]
s4 = sorted(nums, key=lambda x: -x)

print(s1, s2, s3, s4)