# 1. Использование super() для расширения данных
class Person:
    def __init__(self, name, age):
        self.name, self.age = name, age

class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age) # Вызов родителя
        self.subject = subject

# 2. Наследование характеристик электроники
class Electronics:
    def __init__(self, brand): self.brand = brand

class Phone(Electronics):
    def __init__(self, brand, model):
        super().__init__(brand)
        self.model = model

# 3. Базовый платеж и Kaspi
class Payment:
    def __init__(self, amount): self.amount = amount

class KaspiPayment(Payment):
    def __init__(self, amount, phone_number):
        super().__init__(amount)
        self.phone = phone_number

# 4. Сотрудник и менеджер
class Employee:
    def __init__(self, salary): self.salary = salary

class Manager(Employee):
    def __init__(self, salary, bonus):
        super().__init__(salary)
        self.bonus = bonus