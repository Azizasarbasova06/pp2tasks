nums = [1, 2, 3, 4]
# 1. Умножение на 10
res1 = list(map(lambda x: x * 10, nums))
# 2. Превращение в строки
res2 = list(map(lambda x: f"Num {x}", nums))
# 3. Округление списка цен
prices = [10.5, 20.9, 30.1]
res3 = list(map(lambda p: round(p), prices))
# 4. Длина слов в списке
words = ["it", "python", "kbtu"]
res4 = list(map(lambda w: len(w), words))

print(res1, res2, res3, res4)