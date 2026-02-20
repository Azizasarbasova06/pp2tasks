# --- Task 1: Squares of numbers up to N ---
def square_generator(n):
    for i in range(n + 1):
        yield i ** 2

# Пример использования:
n_val = 5
print(f"Squares up to {n_val}:", list(square_generator(n_val)))

print("-" * 30)

# --- Task 2: Even numbers between 0 and n (comma separated) ---
def even_generator(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield str(i)

# Получаем ввод из консоли
n_input = int(input("Enter n for even numbers: "))
# Объединяем результаты через запятую
print(", ".join(even_generator(n_input)))

print("-" * 30)

# --- Task 3: Numbers divisible by 3 and 4 between 0 and n ---
def div_three_four(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

n_div = int(input("Enter n for numbers divisible by 3 and 4: "))
for num in div_three_four(n_div):
    print(f"Found: {num}")

print("-" * 30)

# --- Task 4: Squares from (a) to (b) ---
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

# Тестирование циклом for
start, end = 2, 6
print(f"Yielding squares from {start} to {end}:")
for val in squares(start, end):
    print(val)

print("-" * 30)

# --- Task 5: Countdown from n down to 0 ---
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

n_down = 5
print(f"Countdown from {n_down}:")
for num in countdown(n_down):
    print(num)