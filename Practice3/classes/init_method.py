# 1. Студент с валидацией GPA
class Student:
    def __init__(self, name, sid, gpa):
        self.name = name
        self.sid = sid
        self.gpa = gpa
        print(f"Студент {name} добавлен в базу.")

# 2. Товар в маркетплейсе
class Item:
    def __init__(self, title, price, vendor):
        self.title = title
        self.price = price
        self.vendor = vendor

# 3. Координаты точки доставки
class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

# 4. Книга библиотеки
class Book:
    def __init__(self, title, author, year):
        self.title, self.author, self.year = title, author, year

s = Student("Aziza", "24B01", 3.9)