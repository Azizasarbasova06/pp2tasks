# 1. Базовый класс Пользователь -> Студент
class User:
    def login(self): print("Logged in")

class Student(User):
    def view_grades(self): print("Viewing grades...")

# 2. Еда -> Выпечка
class Food:
    def is_edible(self): return True

class Bakery(Food):
    def bake(self): print("Baking at 180°C")

# 3. Техника -> Ноутбук
class Device:
    def power_on(self): print("On")

class Laptop(Device):
    def close_lid(self): print("Sleep mode")

# 4. Фигура -> Квадрат
class Shape:
    color = "Blue"

class Square(Shape):
    side = 4