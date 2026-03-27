# 1: Generator of squares up to number N
# yield allows the function to return a value and "freeze" until the program asks for the next number.
def square_generator(n):
    for i in range(n + 1):
        yield i ** 2

n_val = 5
print(f"Squares up to {n_val}:", list(square_generator(n_val)))

print("-" * 30)

# 2: Even numbers from 0 to n separated by commas
def even_generator(n):
    for i in range(n + 1):
        if i % 2 == 0:
            # Convert the number to a string to use .join() later.
            yield str(i)

# Input number n from the console
n_input = int(input("Enter n for even numbers: "))
# .join() concatenates all strings from the generator into a single string separated by commas.
print(", ".join(even_generator(n_input)))

print("-" * 30)

# 3: Numbers divisible by 3 and 4 from 0 to n 
def div_three_four(n):
    for i in range(n + 1):
        # Check divisibility by 3 and 4 simultaneously using the % operator.
        if i % 3 == 0 and i % 4 == 0:
            yield i

n_div = int(input("Enter n for numbers divisible by 3 and 4: "))
# We can iterate through the generator directly using a for loop.
for num in div_three_four(n_div):
    print(f"Found: {num}")

print("-" * 30)

# 4: Generator of squares in the range from a to b
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

# Testing the generator with a for loop
start, end = 2, 6
print(f"Yielding squares from {start} to {end}:")
for val in squares(start, end):
    print(val)

print("-" * 30)

# 5: Countdown from n down to 0
def countdown(n):
    while n >= 0:
        yield n
        # Decrease n by 1 in each iteration.
        n -= 1

n_down = 5
print(f"Countdown from {n_down}:")
for num in countdown(n_down):
    print(num)