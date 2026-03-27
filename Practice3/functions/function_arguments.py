# 1. Позиционные аргументы (регистрация студента)
def register_student(name, major):
    print(f"Студент {name} зачислен на факультет {major}.")

# 2. Аргументы по умолчанию (стоимость доставки в SIS)
def calculate_delivery(item, price, fee=500):
    total = price + fee
    print(f"Товар: {item} | Итоговая сумма (с доставкой): {total} KZT")

# 3. Именованные аргументы (настройка профиля)
def update_profile(user_id, email, is_active=True):
    print(f"Профиль #{user_id} ({email}) активен: {is_active}")

# 4. Смешанный тип аргументов
def add_vendor(name, *categories, city="Atyrau"):
    print(f"Вендор {name} из {city} продает: {', '.join(categories)}")

register_student("Aziza", "Information Systems")
calculate_delivery("Домашний пирог", 3500)
update_profile(email="aziza@kbtu.kz", user_id=2401)
add_vendor("Atyrau Delights", "Bakery", "Homemade")