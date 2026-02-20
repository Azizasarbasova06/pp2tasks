# 1. Позиционные аргументы
def student(name, major):
    print(f"{name} studies {major}")

# 2. Аргументы по умолчанию
def get_country(city, country="Kazakhstan"):
    print(f"{city} is in {country}")

# 3. Именованные аргументы (Keyword)
def car_info(brand, model):
    print(f"Car: {brand} {model}")

# 4. Смешивание типов
def shop(item, quantity=1, price=0):
    print(f"Item: {item}, Total: {quantity * price}")

student("Ali", "IS")
get_country("Atyrau")
car_info(model="Camry", brand="Toyota")