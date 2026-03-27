# Импортируем функцию reduce из модуля functools, потому что она не встроена напрямую в Python
from functools import reduce

nums = [1, 2, 3, 4, 5]
print("Список:", nums)

# map() - применяет функцию ко всем элементам
squared = list(map(lambda x: x * x, nums))
print("map (квадраты):", squared)

# filter() - оставляет только чётные числа
even = list(filter(lambda x: x % 2 == 0, nums))
print("filter (чётные):", even)

# reduce() - складывает все элементы
total = reduce(lambda x, y: x + y, nums)
print("reduce (сумма):", total)

# базовые функции
print("len:", len(nums))
print("sum:", sum(nums))
print("min:", min(nums))
print("max:", max(nums))

# преобразование типов
num = "10"
print("int:", int(num))
print("float:", float(num))