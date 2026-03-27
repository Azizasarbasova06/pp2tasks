# 1. Класс Университет
class University:
    name = "KBTU"
    city = "Almaty"

# 2. Класс Продукт для SIS
class Product:
    category = "Homemade Food"
    is_available = True

# 3. Класс Сетевое устройство
class NetworkDevice:
    ip = "192.168.1.1"
    status = "Active"

# 4. Класс Профиль
class UserProfile:
    username = "student"
    credits = 5

uni = University()
print(f"{uni.name} is located in {uni.city}")