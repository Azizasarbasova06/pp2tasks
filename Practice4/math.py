import math
import random

# 1. Встроенные функции (min, max, abs, pow)
nums = [10, 20, 30, -5]
print(f"Max: {max(nums)}, Min: {min(nums)}, Absolute: {abs(-7)}")

# 2. Модуль math (sqrt, ceil, floor, pi)
print(f"Square root of 64: {math.sqrt(64)}")
print(f"Ceil 4.2: {math.ceil(4.2)}, Floor 4.8: {math.floor(4.8)}")
print(f"Value of Pi: {math.pi}")

# 3. Модуль random (randint, choice)
print(f"Random int 1-100: {random.randint(1, 100)}")
colors = ["red", "blue", "green"]
print(f"Random choice: {random.choice(colors)}")

# 4. Перемешивание списка (shuffle)
deck = [1, 2, 3, 4, 5]
random.shuffle(deck)
print(f"Shuffled deck: {deck}")