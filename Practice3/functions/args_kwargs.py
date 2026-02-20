# 1. Использование *args
def sum_all(*args):
    return sum(args)

# 2. Использование **kwargs
def user_data(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

# 3. Комбинация args и обычных
def order_pizza(size, *toppings):
    print(f"Size: {size}, Toppings: {toppings}")

# 4. Полная комбинация
def complex_func(a, *args, **kwargs):
    print(a, args, kwargs)

print(sum_all(1, 2, 3))
user_data(name="Aziza", job="Student")