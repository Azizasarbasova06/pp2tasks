# 1. Простая функция
def greet():
    print("Hello, KBTU!")

# 2. Функция с одним параметром
def welcome_user(name):
    print(f"Welcome, {name}")

# 3. Функция с двумя параметрами
def show_info(city, age):
    print(f"City: {city}, Age: {age}")

# 4. Функция с вызовом другой функции
def main():
    greet()
    print("Main finished")

main()