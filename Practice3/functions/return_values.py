# 1. Возврат числа
def add(a, b):
    return a + b

# 2. Возврат строки
def get_status(score):
    return "Pass" if score > 50 else "Fail"

# 3. Возврат списка
def get_range(n):
    return list(range(n))

# 4. Возврат нескольких значений (кортеж)
def get_min_max(nums):
    return min(nums), max(nums)

print(add(5, 5))
print(get_status(75))
print(get_range(5))
print(get_min_max([1, 2, 3]))